from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_post_list, name='all-posts'),

    path('my_posts/', views.post_list, name='my-posts'),
    path('post/<int:id>/', views.post_detail, name='post-detail'),
]