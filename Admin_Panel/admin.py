from django.contrib import admin
from Users.models import User, Channel
from Content.models import Video, Post, CommentVideo, CommentPost, Playlist, WatchHistory

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['user_type', 'is_active']

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['channel_name', 'user', 'subscribers']
    search_fields = ['channel_name', 'user__username']
    list_filter = ['user']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['video_name', 'channel', 'views', 'created_at']
    search_fields = ['video_name', 'channel__channel_name']
    list_filter = ['channel', 'created_at']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['post_name', 'channel', 'created_at']
    search_fields = ['post_name', 'channel__channel_name']
    list_filter = ['channel', 'created_at']

@admin.register(CommentVideo)
class CommentVideoAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'comment', 'created_at']
    search_fields = ['user__username', 'video__video_name']
    list_filter = ['created_at', 'user']

@admin.register(CommentPost)
class CommentPostAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'comment', 'created_at']
    search_fields = ['user__username', 'post__post_name']
    list_filter = ['created_at', 'user']

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['playlist_name', 'user', 'created_at', 'is_public']
    search_fields = ['playlist_name', 'user__username']
    list_filter = ['is_public', 'created_at']

@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'watched_on', 'duration_watched']
    search_fields = ['user__username', 'video__video_name']
    list_filter = ['watched_on', 'user']
