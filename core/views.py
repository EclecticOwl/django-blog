from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth import views
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

class UserRegistrationView(generic.FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    model = get_user_model()
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.username = form.instance.username.lower()
        form.save()
        messages.success(self.request, 'Account created. Please sign in.')
        return super().form_valid(form)

    def form_invalid(self, form, request):
        messages.error(request, 'It appears some of the information is missing. Please check your entries and try again.')
        return super().form_invalid(form, request)

class SignInView(views.LoginView):
    template_name = 'sign-in.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('index')
    
    def form_valid(self, form):
        messages.success(self.request, 'Signed In!')
        return super().form_valid(form)

class SignOutView(views.LogoutView):
    redirect_authenticated_user = True
    next_page = reverse_lazy('index')

    def get_next_page(self):
        messages.success(self.request, 'Signed Out!')
        return super().get_next_page()

class UserProfileView(generic.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context
        

    

@login_required(login_url='login')
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

@login_required(login_url='login')
def user_list(request):
    profiles = Profile.objects.all()

    context = {'profiles': profiles}
    return render(request, 'users.html', context)

@login_required(login_url='login')
def user_detail(request, pk):
    profile = Profile.objects.get(id=pk)

    if request.method == 'POST':
        if request.user.profile in profile.followers.all():
            request.user.profile.following.remove(profile)
        else:
            request.user.profile.following.add(profile)

    context = {'profile': profile}
    return render(request, 'user_detail.html', context)

@login_required(login_url='login')
def change_password(request):
    user = request.user

    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully. Please re-sign in.')
            return redirect('index')
        else:
            messages.error(request, 'It appears one of the fields was incorrect. Please check your entries and try again.')

    else:
        form = PasswordChangeForm(user)

    context = {'form': form}
    return render(request, 'change_password.html', context)
