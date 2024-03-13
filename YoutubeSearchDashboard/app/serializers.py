from rest_framework import serializers
from .models import Channel, Video, VideoStatistics, ChannelList

class VideoStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoStatistics
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    statistics = VideoStatisticsSerializer(source='videostatistics_set', many=True)

    class Meta:
        model = Video
        fields = ['video_id', 'title', 'description', 'tags', 'deleted', 'statistics']

class ChannelSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(source='video_set', many=True)

    class Meta:
        model = Channel
        fields = ['channel_id', 'channel_name', 'channel_description', 'subscriber_count', 'view_count', 'video_count', 'videos']

class ChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelList
        fields = ['channel_id']
