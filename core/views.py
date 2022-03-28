from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            return redirect('index')

    else:
        form = UserCreationForm()

    context = {}
    return render(request, 'register.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('success')

            return redirect('index')
        else:
            print('Invalid')

    
    context = {}
    return render(request, 'sign-in.html', context)


def signout(request):
    logout(request)
    return redirect('index')
