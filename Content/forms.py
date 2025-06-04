from django import forms
from .models import Video, CommentVideo, Post, Playlist, CommentPost

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_name', 'description', 'category', 'tags', 'thumbnail', 'video_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.TextInput(attrs={'placeholder': 'Comma-separated tags'}),
        }

class CommentVideoForm(forms.ModelForm):
    class Meta:
        model = CommentVideo
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write your comment here...'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_name', 'content', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your post here...'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
        }

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['playlist_name', 'is_public']
        widgets = {
            'playlist_name': forms.TextInput(attrs={'placeholder': 'Playlist Name'}),
        }

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }