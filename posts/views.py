from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Post
from .forms import CustomPostForm

def all_post_list(request):
    posts = Post.objects.all()

    p = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'post_list.html', context)

def post_list(request):
    user = request.user.profile
    posts = Post.objects.filter(owner=user).order_by('-created')

    context = {'posts': posts}
    return render(request, 'my_posts.html', context)

def post_detail(request, id):
    post = Post.objects.get(id=id)

    context = {'post': post}
    return render(request, 'post_detail.html', context)

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

def post_delete(request, id):
    post = request.user.profile.posts.get(id=id)

    if request.method == 'POST':
        print('success')
    context = {'post': post}
    return render(request, 'post_delete.html', context)