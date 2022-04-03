from django.contrib import admin
from .models import Post, Follower


admin.site.register(Post)
admin.site.register(Follower)