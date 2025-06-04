from django.db import models
from Users.models import Channel, User
from django.conf import settings


class Video(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    video_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    video_file = models.FileField(upload_to='videos/')
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_name
    
class Post(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    post_name = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.CharField(max_length=255, blank=True)
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_name

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=30)
    videos = models.ManyToManyField(Video)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.playlist_name} by {self.user}'
    
class CommentVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.TextField()
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.video}'
    
class CommentPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
    
class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_on = models.DateTimeField(auto_now_add=True)
    duration_watched = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user} watched {self.video}'
    

class VideoInteraction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    ACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f'{self.user.username} - {self.action} - {self.video.video_name}'