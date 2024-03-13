from django.contrib import admin
from .models import Channel, Video, VideoStatistics, ChannelList

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['channel_id', 'channel_name', 'subscriber_count', 'view_count', 'video_count']
    search_fields = ['channel_id', 'channel_name']
    list_filter = ['subscriber_count', 'view_count', 'video_count']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['video_id', 'title', 'channel', 'deleted']
    search_fields = ['video_id', 'title', 'channel__channel_id', 'channel__channel_name']
    list_filter = ['deleted']

@admin.register(VideoStatistics)
class VideoStatisticsAdmin(admin.ModelAdmin):
    list_display = ['video', 'view_count', 'like_count', 'favorite_count', 'comment_count', 'timestamp']
    search_fields = ['video__video_id', 'video__title']
    list_filter = ['timestamp']

@admin.register(ChannelList)
class ChannelListAdmin(admin.ModelAdmin):
    list_display = ['channel_id']
    search_fields = ['channel_id']
