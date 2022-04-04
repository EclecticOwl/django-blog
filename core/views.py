from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Profile
from posts.models import Post
from posts.forms import CustomPostForm

from .forms import ProfileForm

def index(request):
    if request.user.is_anonymous:
        context = {}
    else:
        profile_followers = request.user.profile.following.all()
        profile_feed = Post.objects.filter(owner_id__in=profile_followers).order_by('-created')

        form = CustomPostForm()
        
        if request.method == 'POST':
            form = CustomPostForm(request.POST)

            if form.is_valid():

                user = form.save(commit=False)
                user.owner = request.user.profile
                user.save()

                messages.success(request, 'New post created successfully!')
                
            else:
                print('Error')
        else:
            form
        context = {'profile_feed': profile_feed, 'form': form}
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            messages.success(request, 'User created successfully. Please sign in.')
            return redirect('index')
        else:
            messages.error(request, 'It appears some of your information was incorrect. Please check and resubmit.')

    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)

def signin(request):
    if request.user.is_authenticated == True:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully signed in!')

            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password. Please re-check your entries and try again.')

    
    context = {}
    return render(request, 'sign-in.html', context)

def signout(request):
    logout(request)
    messages.success(request, 'You successfully signed out.')
    return redirect('index')

def user_profile(request):
    profile = request.user.profile


    context = {'profile': profile}
    return render(request, 'profile.html', context)

def edit_user_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
           form.save()
           messages.success(request, "Information successfully updated!")
           return redirect('user-profile')
        else:
            messages.error(request, "It appears that something went wrong with the request. Please check your entries and re-submit.")


    context = {'profile': profile, 'form': form}
    return render(request, 'edit_profile.html', context)

def user_list(request):
    profiles = Profile.objects.all()

    context = {'profiles': profiles}
    return render(request, 'users.html', context)

def user_detail(request, pk):
    profile = Profile.objects.get(id=pk)


    context = {'profile': profile}
    return render(request, 'user_detail.html', context)

