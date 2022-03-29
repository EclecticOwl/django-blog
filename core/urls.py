from django.urls import path

from . import views


urlpatterns = [
    path('', views.index , name='index'),

    # Authentication Views
    path('register/', views.register , name='register'),
    path('sign-in/', views.signin, name='login'),
    path('sign-out/', views.signout, name='logout'),

    path('profile/', views.user_profile, name='user-profile'),
    path('profile/edit', views.edit_user_profile, name='update-user-profile'),
]
