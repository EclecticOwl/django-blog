from django.urls import path

from . import views

urlpatterns = [
    path('inbox/', views.message_inbox, name='message_inbox'),
    path('user/<int:id>/', views.message_detail, name='message_detail'),
]