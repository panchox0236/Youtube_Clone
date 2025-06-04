from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('delete_account/', views.delete_account_view, name='delete_account'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('become_creator/', views.become_creator_view, name='become_creator'),
    path('profile/', views.edit_profile_view, name='profile'), 
    path('create_channel/', views.create_channel_view, name='create_channel'),
    path('become_creator/', views.become_creator_view, name='become_creator'),
]
