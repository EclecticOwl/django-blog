from django.db import models
from core.models import Profile


class Post(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    description = models.CharField(max_length=100)
    content = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description
