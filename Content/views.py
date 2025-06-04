import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CommentVideo, Video, Post, Playlist, WatchHistory, CommentPost, VideoInteraction
from Users.models import Channel,User
from .forms import VideoForm, CommentVideoForm, PostForm, PlaylistForm, CommentPostForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.utils import timezone
from django.views.decorators.http import require_POST


@login_required
def upload_video_view(request):
    if request.user.user_type != User.CREATOR:
        messages.error(request, 'You must be a content creator to upload videos.')
        return redirect('home')

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.channel = request.user.channel 
            video.save()
            messages.success(request, 'Video uploaded successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Failed to upload video. Please check the form for errors.')
    else:
        form = VideoForm()

    return render(request, 'content/upload_video.html', {'form': form})

@login_required
def create_post_view(request):
    if request.user.user_type != 'creator':
        return redirect('home')

    channel = get_object_or_404(Channel, user=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.channel = channel
            post.save()
            return redirect('view_post', post_id=post.id)
    else:
        form = PostForm()

    return render(request, 'content/create_post.html', {'form': form})

def watch_video_view(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    playlists = None

    video.views += 1
    video.save()

    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(user=request.user)
        WatchHistory.objects.create(
            user=request.user,
            video=video,
            watched_on=timezone.now(),
            duration_watched=0
        )

    return render(request, 'content/watch_video.html', {'video': video, 'playlists': playlists})

def view_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'content/view_posts.html', {'posts': posts})

def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = CommentPost.objects.filter(post=post).order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentPostForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect('view_post', post_id=post.id)
        else:
            return redirect('login')

    else:
        form = CommentPostForm()

    return render(request, 'content/view_post.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def manage_playlist_view(request):
    if request.method == 'POST':
        playlist_name = request.POST['playlist_name']
        video_id = request.POST.get('video_id')

        try:
            video_id = int(video_id)  
            video = get_object_or_404(Video, pk=video_id)
        except ValueError:
            messages.error(request, 'Invalid video ID.')
            return redirect('manage_playlist')

        Playlist.objects.create(fk_username=request.user.username, fk_video_id=video, playlist_name=playlist_name)
        messages.success(request, 'Video added to playlist successfully!')
        return redirect('home')
    
    playlists = Playlist.objects.filter(fk_username=request.user.username)
    return render(request, 'content/manage_playlist.html', {'playlists': playlists})

@login_required
def watch_history_view(request):
    watch_history = WatchHistory.objects.filter(user=request.user).order_by('-watched_on').select_related('video')
    return render(request, 'content/watch_history.html', {'watch_history': watch_history})

@login_required
@csrf_exempt
def create_comment_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment_text = data.get('comment', '')

            if comment_text:
                comment = CommentVideo.objects.create(
                    user=request.user,
                    video=video,
                    comment=comment_text
                )
                
                return JsonResponse({
                    'success': True,
                    'user': request.user.username,
                    'comment': comment.comment,
                })
            else:
                return JsonResponse({'success': False, 'error': 'Comment text is required'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@require_POST
@login_required
def like_dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    action = request.POST.get('action')

    interaction, created = VideoInteraction.objects.get_or_create(user=request.user, video=video)

    if not created:
        if interaction.action == action:
            interaction.delete()
            if action == 'like':
                video.like -= 1
            elif action == 'dislike':
                video.dislike -= 1
        else:
            if interaction.action == 'like':
                video.like -= 1
            elif interaction.action == 'dislike':
                video.dislike -= 1

            interaction.action = action
            interaction.save()

            if action == 'like':
                video.like += 1
            elif action == 'dislike':
                video.dislike += 1
    else:
        interaction.action = action
        interaction.save()
        if action == 'like':
            video.like += 1
        elif action == 'dislike':
            video.dislike += 1

    video.save()

    return JsonResponse({'likes': video.like, 'dislikes': video.dislike})
    
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if 'like' in request.POST:
            post.like += 1
        elif 'dislike' in request.POST:
            post.dislike += 1
        post.save()
        return JsonResponse({'likes': post.like, 'dislikes': post.dislike})

@login_required
def create_playlist_view(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            messages.success(request, 'Playlist created successfully.')
            return redirect('manage_playlist')
    else:
        form = PlaylistForm()

    return render(request, 'content/create_playlist.html', {'form': form})

@login_required
def manage_playlist_view(request):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist_id')
        video_id = request.POST.get('video_id')
        
        if playlist_id and video_id:
            try:
                playlist = Playlist.objects.get(id=playlist_id, user=request.user)
                video = Video.objects.get(id=video_id)
                playlist.videos.add(video)
                messages.success(request, 'Video added to playlist successfully.')
            except Playlist.DoesNotExist:
                messages.error(request, 'Playlist does not exist.')
            except Video.DoesNotExist:
                messages.error(request, 'Video does not exist.')
    
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'content/manage_playlist.html', {'playlists': playlists})


def search_videos(request):
    query = request.GET.get('query', '')
    results = Video.objects.filter(video_name__icontains=query) if query else []
    return render(request, 'content/search_results.html', {'query': query, 'results': results})

@login_required
def list_playlists_view(request):
    playlists = Playlist.objects.filter(user=request.user).prefetch_related('videos')
    return render(request, 'content/list_playlists.html', {'playlists': playlists})

@login_required
def playlist_videos_view(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    videos = playlist.videos.all()
    return render(request, 'content/playlist_videos.html', {'playlist': playlist, 'videos': videos})
