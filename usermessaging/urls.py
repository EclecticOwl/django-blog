from django.urls import path

from . import views

urlpatterns = [
    path('', views.MessageHomeView.as_view(), name="messages_home"),

    path('inbox/', views.MessageInboxView.as_view(), name='message_inbox'),
    path('outbox/', views.MessageOutboxView.as_view(), name='message_outbox'),
    path('inbox/<int:pk>/', views.MessageInboxDetailView.as_view(), name='message_detail_inbox'),
    path('outbox/<int:id>/', views.message_detail_outbox, name='message_detail_outbox'),

    path('new_message/<int:id>/', views.send_message, name='send_message'),
]