from django.urls import path
from .views import (
    fetch_and_store_channel_data,
    fetch_and_store_video_data,
    fetch_and_store_video_statistics,
    get_channel_data,
    get_video_statistics_data,
    get_channel_list_data,
    get_total_views,
    get_channel_videos,
    get_channel_list,
    get_channel_by_name,
    get_all_video_stats,
    get_video_stats_by_id,
    get_channels_in_table,
    search_video_by_title,
)

urlpatterns = [
    #Endpoint for channel_id
    path('channel_by_name/<str:channel_name>/', get_channel_by_name, name='channel_by_name'),
    # Endpoints for fetching and storing data
    path('fetch_and_store_channels/', fetch_and_store_channel_data, name='fetch_and_store_channels'),
    path('fetch_and_store_videos/', fetch_and_store_video_data, name='fetch_and_store_videos'),
    path('fetch_and_store_video_statistics/', fetch_and_store_video_statistics, name='fetch_and_store_video_statistics'),

    # Endpoints for retrieving data
    path('get_channels/', get_channel_data, name='get_channels_data(you will find all the channels data here)'),
    path('get_video_statistics/', get_video_statistics_data, name='get_video_statistics'),
    path('get_channel_list/', get_channel_list_data, name='get_channel_list'),
    path('channels/', get_channels_in_table, name='get_channels'),

    # Endpoints for custom queries
    path('total_views/<str:channel_id>/<str:start_timestamp>/<str:end_timestamp>/', get_total_views, name='total_views'),
    path('channel_videos/<str:channel_id>/', get_channel_videos, name='channel_videos'),
    path('channel_list/', get_channel_list, name='channel_list'),

    #for 1 video

    path('get_all_video_stats/<str:video_id>/', get_all_video_stats, name='get_all_video_stats'),
    path('get_video_stats_by_id/<str:video_id>/', get_video_stats_by_id, name='get_video_stats_by_id'),
    
    path('api/search_video_by_title/<str:search_query>', search_video_by_title, name='search_video_by_title'),

]
