from django.urls import path
from . import views


urlpatterns = [
    path('', views.AllPostListView.as_view(), name='all-posts'),

    path('my-posts/', views.MyPostListView.as_view(), name='my-posts'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/update/<int:pk>/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),
]