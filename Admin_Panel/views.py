from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from Users.models import User, Channel
from Content.models import Video, Post, Playlist, WatchHistory
from django.contrib import messages


admin_required = user_passes_test(lambda u: u.is_superuser)


@admin_required
def admin_panel_view(request):
    users = User.objects.all()
    channels = Channel.objects.all()
    videos = Video.objects.all()
    posts = Post.objects.all()
    return render(request, 'admin_panel/admin_dashboard.html', {
        'users': users,
        'channels': channels,
        'videos': videos,
        'posts': posts
    })


@admin_required
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('admin_panel')


@admin_required
def delete_channel_view(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)
    channel.delete()
    messages.success(request, 'Channel deleted successfully!')
    return redirect('admin_panel')


@admin_required
def delete_video_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.delete()
    messages.success(request, 'Video deleted successfully!')
    return redirect('admin_panel')


@admin_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('admin_panel')

@admin_required
def manage_watch_history_view(request):
    watch_history = WatchHistory.objects.all().order_by('-watched_on')
    return render(request, 'admin_panel/manage_watch_history.html', {'watch_history': watch_history})
