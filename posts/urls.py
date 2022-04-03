from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_post_list, name='all-posts'),

    path('my_posts/', views.my_posts, name='my-posts'),
]