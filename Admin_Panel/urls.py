from django.urls import path
from . import views 

urlpatterns = [
    path('', views.admin_panel_view, name='admin_panel'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('delete_channel/<int:channel_id>/', views.delete_channel_view, name='delete_channel'),
    path('delete_video/<int:video_id>/', views.delete_video_view, name='delete_video'),
    path('delete_post/<int:post_id>/', views.delete_post_view, name='delete_post'),
]
