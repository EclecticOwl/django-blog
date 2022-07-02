from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.views import generic
from django.contrib.auth import views, get_user_model

from posts.models import Post
from posts.forms import CustomPostForm

from .forms import ProfileForm, ThemeForm
from .models import Profile


UserModel = get_user_model()


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

class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context
        

class EditUserProfileView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'edit_profile.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('user-profile')

    def get_queryset(self):
        queryset = Profile.objects.filter(id=self.request.user.profile.id)
        return queryset
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user.profile = self.request.user.profile
        form.save()
        messages.success(self.request, 'Profile Updated')
        return super().form_valid(form)
    
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

class ChangePassView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(self.request, 'Password has been updated.')
        return form


def UpdateTheme(request):
    theme = request.user.profile
    form = ThemeForm(instance=theme)

    if request.method == 'POST':
        form = ThemeForm(instance=theme, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Theme Updated')



    context = {'form': form, 'theme': theme}
    return render(request, 'change_theme.html', context)