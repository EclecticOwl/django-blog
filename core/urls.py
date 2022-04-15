from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name='index'),

    # Authentication Views
    path('register/', views.UserRegistrationView.as_view() , name='register'),
    path('sign-in/', views.SignInView.as_view() , name='login'),
    path('sign-out/', views.SignOutView.as_view() , name='logout'),
    path('change-password/', views.ChangePassView.as_view(), name='change-password'),

    path('account/', views.UserProfileView.as_view() , name='user-profile'),
    path('account/edit/<int:pk>/', views.EditUserProfileView.as_view() , name='update-user-profile'),

    path('users/<pk>/', views.user_detail, name='user-detail'),
]
