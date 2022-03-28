from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

def index(request):
    return render(request, 'index.html')


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
