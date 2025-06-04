from django.urls import path
from . import views

urlpatterns = [
    path('upload_video/', views.upload_video_view, name='upload_video'),
    path('watch_video/<int:video_id>/', views.watch_video_view, name='watch_video'),
    path('watch_video/<int:video_id>/comment/', views.create_comment_view, name='create_comment'),
    path('create_post/', views.create_post_view, name='create_post'),
    path('posts/', views.view_posts, name='view_posts'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('watch_history/', views.watch_history_view, name='watch_history'),
    path('create_playlist/', views.create_playlist_view, name='create_playlist'),
    path('manage_playlist/', views.manage_playlist_view, name='manage_playlist'),
    path('playlists/', views.list_playlists_view, name='list_playlists'),
    path('playlist/<int:playlist_id>/', views.playlist_videos_view, name='playlist_videos'),
    path('watch_video/<int:video_id>/like_dislike/', views.like_dislike_video, name='like_dislike_video'),
    path('search/', views.search_videos, name='search_videos'),
]
