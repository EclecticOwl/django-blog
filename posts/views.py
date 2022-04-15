from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic


from .models import Post
from .forms import CustomPostForm

class AllPostListView(LoginRequiredMixin, generic.ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 4

class MyPostListView(LoginRequiredMixin, generic.ListView):
    template_name = 'my_posts.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user.profile).order_by('-created')

class PostDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'post_detail.html'
    model = Post

class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'post_update.html'
    model = Post
    form_class = CustomPostForm
    success_url = reverse_lazy('my-posts')

    def form_valid(self, form):
        form = super().form_valid(form)
        messages.success(self.request, 'Post Updated!')
        return form



@login_required(login_url='login')
def post_delete(request, id):
    post = request.user.profile.posts.get(id=id)

    if request.method == 'POST':
        print('success')
    context = {'post': post}
    return render(request, 'post_delete.html', context)