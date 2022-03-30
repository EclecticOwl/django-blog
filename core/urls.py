from django.urls import path

from . import views


urlpatterns = [
    path('', views.index , name='index'),

    # Authentication Views
    path('register/', views.register , name='register'),
    path('sign-in/', views.signin, name='login'),
    path('sign-out/', views.signout, name='logout'),

    path('account/', views.user_profile, name='user-profile'),
    path('account/edit', views.edit_user_profile, name='update-user-profile'),

    path('users/', views.user_list, name='user-list'),
    path('users/<int:pk>/', views.user_detail, name='user-detail'),
]
