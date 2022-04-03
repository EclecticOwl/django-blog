from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Post

def latest_post_list(request):
    posts = Post.objects.all().order_by('-created')

    p = Paginator(posts, 4)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'post_list.html', context)