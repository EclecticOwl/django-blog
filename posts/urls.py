from django.urls import path
from . import views


urlpatterns = [
    path('', views.latest_post_list, name='all-posts'),
]