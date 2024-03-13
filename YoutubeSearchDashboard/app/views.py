import datetime
import json
import requests
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .models import Channel, Video, VideoStatistics, ChannelList
from .serializers import ChannelSerializer, VideoSerializer, VideoStatisticsSerializer, ChannelListSerializer
from .constants import api_key_channel_and_videos, api_key_video_statistics
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime

@api_view(['GET'])
def get_all_video_stats(request, video_id):
    try:
        # Get all the video statistics for the given video_id
        video_stats = VideoStatistics.objects.filter(video__video_id=video_id)

        # Prepare the result to hold all video statistics
        result = {
            'video_id': video_id,
            'video_stats': []
        }

        # Iterate through the video statistics and add them to the result
        for stats in video_stats:
            stats_data = {
                'id': stats.id,
                'view_count': stats.view_count,
                'like_count': stats.like_count,
                'favorite_count': stats.favorite_count,
                'comment_count': stats.comment_count,
                'timestamp': stats.timestamp,
            }
            result['video_stats'].append(stats_data)

        return Response(result)

    except VideoStatistics.DoesNotExist:
        return Response({'error': 'Video statistics not found for the given video_id.'}, status=404)

def get_video_stats(request, video_id, start_timestamp, end_timestamp):
    # Convert the start and end timestamps to datetime objects
    start_datetime = datetime.strptime(start_timestamp, '%Y-%m-%d %H:%M:%S')
    end_datetime = datetime.strptime(end_timestamp, '%Y-%m-%d %H:%M:%S')

    # Get the video object based on the video_id
    video = get_object_or_404(Video, video_id=video_id)

    # Fetch the video statistics within the given time interval
    video_stats = VideoStatistics.objects.filter(
        video=video,
        timestamp__gte=start_datetime,
        timestamp__lte=end_datetime
    )

    # Prepare the response data
    response_data = {
        'video_id': video.video_id,
        'start_timestamp': start_timestamp,
        'end_timestamp': end_timestamp,
        'stats': []
    }

    # Add video statistics to the response data
    for stat in video_stats:
        response_data['stats'].append({
            'timestamp': stat.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'view_count': stat.view_count,
            'like_count': stat.like_count,
            'favorite_count': stat.favorite_count,
            'comment_count': stat.comment_count
        })

    return JsonResponse(response_data)

@api_view(['GET'])
def fetch_and_store_channel_data(request):
    try:
        db_channels = ChannelList.objects.all()
        values = []  # Initialize an empty list for bulk insert

        for channel in db_channels:
            channel_stats = _get_channels_data(channel.channel_id, 'snippet,statistics,contentDetails')
            if 'items' in channel_stats:
                channel_item = channel_stats['items'][0]
                channel_name = channel_item['snippet']['title']
                channel_id = channel_item['id']
                uploads_playlist_id = channel_item['contentDetails']['relatedPlaylists']['uploads']
                channel_description = channel_item['snippet']['description']
                subscriber_count = channel_item['statistics'].get('subscriberCount', 0)
                view_count = channel_item['statistics'].get('viewCount', 0)
                video_count = channel_item['statistics'].get('videoCount', 0)

                # Append values for bulk insert
                values.append(Channel(
                    channel_name=channel_name,
                    channel_id=channel_id,
                    uploads_playlist_id=uploads_playlist_id,
                    channel_description=channel_description,
                    subscriber_count=subscriber_count,
                    view_count=view_count,
                    video_count=video_count
                ))

        # Perform bulk insert
        if values:
            Channel.objects.bulk_create(values, ignore_conflicts=True)

        return Response("Channel data fetched and stored successfully.")
    except Exception as e:
        print("Error occurred while fetching and storing channel data:", e)
        return Response("An error occurred while fetching and storing channel data.")
    
@api_view(['GET'])
def get_channel_by_name(request, channel_name):

    search_url = f"https://youtube.googleapis.com/youtube/v3/search"
    params = {
        'part': 'id',
        'q': channel_name,
        'type': 'channel',
        'key': api_key_channel_and_videos,
    }

    try:
        response = requests.get(search_url, params=params)
        response_json = response.json()

        if 'items' in response_json:
            items = response_json['items']
            if items:
                channel_id = items[0]['id']['channelId']
                return JsonResponse({'channel_id': channel_id})
            else:
                return JsonResponse({'error': 'No channel found for the given name.'}, status=404)
        else:
            return JsonResponse({'error': 'Error in API response.'}, status=500)

    except requests.RequestException:
        return JsonResponse({'error': 'Error in making API request.'}, status=500)


@api_view(['GET'])
def fetch_and_store_video_data(request):
    try:
        db_channels = Channel.objects.all()
        values = []  # Initialize an empty list for bulk insert

        for channel in db_channels:
            channel_videos = _get_channel_content(channel.uploads_playlist_id, limit=50, check_all_pages=True)
            for video_id, video_info in channel_videos.items():
                video = Video(
                    video_id=video_id,
                    channel=channel,
                    title=video_info['title'],
                    description=video_info['description'],
                    tags='',
                    deleted=False
                )
                values.append(video)

        # Perform bulk insert
        if values:
            Video.objects.bulk_create(values, ignore_conflicts=True)

        return Response("Video data fetched and stored successfully.")
    except Exception as e:
        print("Error occurred while fetching and storing video data:", e)
        return Response(f"Error fetching and storing video data: {str(e)}")


@api_view(['GET'])
def fetch_and_store_video_statistics(request):
    try:
        db_videos = Video.objects.all()
        values = []  # Initialize an empty list for bulk insert

        for video in db_videos:
            video_stats = _get_single_video_data(video.video_id, 'statistics')
            if 'items' in video_stats:
                item = video_stats['items'][0]
                video_stat = VideoStatistics(
                    video=video,
                    view_count=item['statistics'].get('viewCount', 0),
                    like_count=item['statistics'].get('likeCount', 0),
                    favorite_count=item['statistics'].get('favoriteCount', 0),
                    comment_count=item['statistics'].get('commentCount', 0),
                    timestamp=datetime.now()  # Use datetime from the imported module
                )
                values.append(video_stat)

        # Perform bulk insert
        if values:
            VideoStatistics.objects.bulk_create(values, ignore_conflicts=True)

        return Response("Video statistics fetched and stored successfully.")
    except Exception as e:
        print("Error occurred while fetching and storing video statistics:", e)
        return Response(f"Error fetching and storing video statistics: {str(e)}")

def _get_channels_data(channel_id_list, parts):
    try:
        channel_url = f"https://youtube.googleapis.com/youtube/v3/channels?part={parts}&id={channel_id_list}&key={api_key_channel_and_videos}"
        json_url = requests.get(channel_url)
        channel_content = json.loads(json_url.text)
    except Exception as e:
        print(f'Error! Could not get {parts} data: \n{channel_id_list}')
        print("Exception:", e)
        channel_content = dict()
    return channel_content


def _get_channel_content(uploads_playlist_id, limit=None, check_all_pages=True):
    url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?" \
          f"part=contentDetails,snippet&playlistId={uploads_playlist_id}&" \
          f"key={api_key_channel_and_videos}"
    if limit is not None and isinstance(limit, int):
        url += "&maxResults=" + str(limit)

    channel_videos, npt = _get_channel_content_per_page(url)
    while check_all_pages and npt is not None:
        next_url = url + "&pageToken=" + npt
        next_vid, npt = _get_channel_content_per_page(next_url)
        channel_videos.update(next_vid)

    return channel_videos


def _get_channel_content_per_page(url):
    try:
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()
        if 'items' not in data:
            print('Error! Could not get correct channel data!\n', data)
            return channel_videos, None

        nextPageToken = data.get("nextPageToken", None)

        item_data = data['items']
        for item in item_data:
            try:
                video_title = item['snippet']['title']
                channel_id = item['snippet']['channelId']
                video_description = item['snippet']['description']
                video_id = item['contentDetails']['videoId']
                channel_videos[video_id] = {
                    'title': video_title,
                    'channel_id': channel_id,
                    'description': video_description
                }
            except KeyError as error:
                print(f'Error! Could not extract data from item:{item} and error is {error}')

        return channel_videos, nextPageToken

    except Exception as e:
        print("Error occurred while fetching channel content:", e)
        return dict(), None


def _get_single_video_data(video_id, parts):
    try:
        url = f"https://www.googleapis.com/youtube/v3/videos?part={parts}&id={video_id}&key={api_key_video_statistics}"
        json_url = requests.get(url)
        video_content = json.loads(json_url.text)
    except Exception as e:
        print(f'Error! Could not get {parts} data: \n{video_id}')
        print("Exception:", e)
        video_content = dict()
    return video_content


@api_view(['GET'])
def get_total_views(request, channel_id, start_timestamp, end_timestamp):
    # Convert the start_timestamp and end_timestamp to timezone-aware datetime objects
    start_timestamp = timezone.make_aware(datetime.strptime(start_timestamp, "%Y-%m-%d %H:%M:%S"))
    end_timestamp = timezone.make_aware(datetime.strptime(end_timestamp, "%Y-%m-%d %H:%M:%S"))

    total_views = VideoStatistics.objects.filter(
        video__channel__channel_id=channel_id, 
        timestamp__range=[start_timestamp, end_timestamp]
    ).aggregate(total_views=Sum('view_count'))

    if total_views['total_views'] is not None:
        return Response(total_views)
    else:
        return Response({'error': 'No data found for given parameters.'}, status=400)

@api_view(['GET'])
def get_video_stats_by_id(request, video_id=None):
    try:
        # Fetch video by video ID if provided, else fetch all videos
        if video_id:
            video = get_object_or_404(Video, video_id=video_id)
            videos = [video]
        else:
            videos = Video.objects.all()

        values = []  # Initialize an empty list for bulk insert

        for video in videos:
            video_stats = _get_single_video_data(video.video_id, 'statistics')
            if 'items' in video_stats:
                item = video_stats['items'][0]
                video_stat = VideoStatistics(
                    video=video,
                    view_count=item['statistics'].get('viewCount', 0),
                    like_count=item['statistics'].get('likeCount', 0),
                    favorite_count=item['statistics'].get('favoriteCount', 0),
                    comment_count=item['statistics'].get('commentCount', 0),
                    timestamp=datetime.now()  # Use datetime from the imported module
                )
                values.append(video_stat)

        # Perform bulk insert
        if values:
            VideoStatistics.objects.bulk_create(values, ignore_conflicts=True)

        return Response("Video statistics fetched and stored successfully.")
    except Exception as e:
        print("Error occurred while fetching and storing video statistics:", e)
        return Response(f"Error fetching and storing video statistics: {str(e)}")

@api_view(['GET'])
def get_channel_videos(request, channel_id):
    try:
        channel = Channel.objects.get(channel_id=channel_id)
        videos = Video.objects.filter(channel=channel)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    except Channel.DoesNotExist:
        return Response({'error': 'Channel not found.'}, status=404)


@api_view(['GET'])
def get_video_statistics(request, video_id):
    try:
        video = Video.objects.get(video_id=video_id)
        statistics = VideoStatistics.objects.filter(video=video)
        serializer = VideoStatisticsSerializer(statistics, many=True)
        return Response(serializer.data)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found.'}, status=404)


@api_view(['GET'])
def get_channel_list(request):
    channel_list = ChannelList.objects.all()
    serializer = ChannelListSerializer(channel_list, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_channel_data(request):
    channels = Channel.objects.all()
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)




@api_view(['GET'])
def get_video_statistics_data(request):
    video_stats = VideoStatistics.objects.all()
    serializer = VideoStatisticsSerializer(video_stats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_channel_list_data(request):
    channel_list = ChannelList.objects.all()
    serializer = ChannelListSerializer(channel_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_channels_in_table(request):
    channels = Channel.objects.all()
    serializer = ChannelSerializer(channels, many=True)
    return Response(serializer.data)

from html import unescape  # Import unescape function to handle HTML characters

@api_view(['GET'])
def search_video_by_title(request, search_query):
    try:
        # Unescape the HTML characters in the search query
        search_query = unescape(search_query)

        # Filter videos by title containing the search query
        videos = Video.objects.filter(title__icontains=search_query)

        # Prepare the response data
        response_data = []
        for video in videos:
            # Use unescape to handle HTML characters in the title and description
            title = unescape(video.title)
            description = unescape(video.description)
            video_data = {
                'video_id': video.video_id,
                'title': title,
                'description': description
            }
            response_data.append(video_data)

        return Response(response_data)

    except Exception as e:
        print("Error occurred while searching for videos:", e)
        return Response({'error': 'An error occurred while searching for videos.'}, status=500)

