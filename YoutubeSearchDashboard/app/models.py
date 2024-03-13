
from datetime import datetime
from django.db import models

class Channel(models.Model):
    channel_name = models.CharField(max_length=50)
    channel_id = models.CharField(max_length=50, unique=True)
    uploads_playlist_id = models.CharField(max_length=50)
    channel_description = models.TextField()
    subscriber_count = models.BigIntegerField()
    view_count = models.BigIntegerField()
    video_count = models.BigIntegerField()

class Video(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    title = models.CharField(max_length=5000)
    description = models.TextField()
    tags = models.CharField(max_length=500)
    deleted = models.BooleanField(default=False)

class VideoStatistics(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    view_count = models.BigIntegerField()
    like_count = models.BigIntegerField()
    favorite_count = models.BigIntegerField()
    comment_count = models.BigIntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.video.title} - {self.timestamp}"

class ChannelList(models.Model):
    channel_id = models.CharField(max_length=50, unique=True)
    start_date = models.DateTimeField(null=True, default=datetime.now)  # Make start_date nullable
    end_date = models.DateTimeField(null=True, blank=True)  # Make end_date nullable


    def __str__(self):
        return self.channel_id
