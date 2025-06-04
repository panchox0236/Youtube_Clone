from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Channel
from .forms import UserRegistrationForm, ChannelForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'users/login.html')


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(form.cleaned_data['password'])

            user_type_str = form.cleaned_data.get('user_type') 
            
            if user_type_str in dict(User.USER_TYPE_CHOICES).keys():
                user.user_type = user_type_str
            else:
                user.user_type = User.STANDARD
            
            user.save()
            
            login(request, user)
            messages.success(request, 'Registration successful.')
            
            if user.user_type == User.CREATOR:
                return redirect('create_channel')
            
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please check the form for errors.')
            print(form.errors)

    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def delete_account_view(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('register')
    return render(request, 'users/delete_account.html')

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.email = request.POST['email']
        user.profile_pic = request.FILES.get('profile_pic')
        user.bio = request.POST['bio']
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    return render(request, 'users/edit_profile.html', {'user': user})

@login_required
def become_creator_view(request):
    user = request.user
    if user.user_type == User.STANDARD:
        if request.method == 'POST':
            form = ChannelForm(request.POST)
            if form.is_valid():
                user.user_type = User.CREATOR
                user.save()
                channel = form.save(commit=False)
                channel.user = user
                channel.save()

                messages.success(request, 'You are now a content creator and your channel has been created.')
                return redirect('profile')
        else:
            form = ChannelForm()
        return render(request, 'users/become_creator.html', {'form': form})
    else:
        messages.error(request, 'You are already a content creator.')
        return redirect('profile')

@login_required
def create_channel_view(request):
    user = request.user
    if user.user_type != User.CREATOR:
        messages.error(request, 'You are not authorized to create a channel.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.user = user
            channel.save()
            messages.success(request, 'Channel created successfully.')
            return redirect('profile')
    else:
        form = ChannelForm()
    
    return render(request, 'users/create_channel.html', {'form': form})