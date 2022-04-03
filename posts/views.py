from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Post

def all_post_list(request):
    posts = Post.objects.filter(owner=request.user)

    p = Paginator(posts, 4)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'post_list.html', context)

def my_posts(request):
    user = request.user.profile

    posts = Post.objects.filter(owner=user)

    context = {'posts': posts}
    return render(request, 'my_posts.html', context)