from django.urls import path

from . import views

urlpatterns = [
    path('inbox/', views.message_inbox, name='message_inbox'),
    path('outbox/', views.message_outbox, name='message_outbox'),
    path('inbox/<int:id>/', views.message_detail_inbox, name='message_detail_inbox'),
    path('outbox/<int:id>/', views.message_detail_outbox, name='message_detail_outbox'),

    path('new_message/<int:id>/', views.send_message, name='send_message'),
]