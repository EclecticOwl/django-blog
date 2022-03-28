from django.urls import path

from . import views


urlpatterns = [
    path('', views.index , name='index'),

    # Authentication Views
    path('register/', views.register , name='register'),
    path('sign-in/', views.signin, name='login'),
    path('sign-out/', views.signout, name='logout'),
]
