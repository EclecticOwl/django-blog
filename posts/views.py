from django.shortcuts import render, redirect
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

@login_required(login_url='login')
def post_detail(request, id):
    post = Post.objects.get(id=id)

    context = {'post': post}
    return render(request, 'post_detail.html', context)

@login_required(login_url='login')
def post_update(request, id):
    post = request.user.profile.posts.get(id=id)

    if request.method == 'POST':
        form = CustomPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('my-posts')
    else:
        form = CustomPostForm(instance=post)

    context = {'post': post, 'form': form}
    return render(request, 'post_update.html', context)

@login_required(login_url='login')
def post_delete(request, id):
    post = request.user.profile.posts.get(id=id)

    if request.method == 'POST':
        print('success')
    context = {'post': post}
    return render(request, 'post_delete.html', context)