from django.db import models
from core.models import Profile

class Message(models.Model):
    sender = models.ForeignKey(Profile, related_name='sender', on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(Profile, related_name='receiver', on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=100)
    content = models.TextField(max_length=400)
    is_read = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'From {self.sender.username} to {self.receiver.username}'