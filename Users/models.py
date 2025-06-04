from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMIN = 'admin'
    CREATOR = 'creator'
    STANDARD = 'standard'
    USER_TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (CREATOR, 'Content Creator'),
        (STANDARD, 'Standard User'),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=STANDARD)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.username

    class Meta:
        swappable = 'AUTH_USER_MODEL'

class Channel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    subscribers = models.PositiveIntegerField(default=0)
    channel_pic = models.ImageField(upload_to='channel_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.channel_name
