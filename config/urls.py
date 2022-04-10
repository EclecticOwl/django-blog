from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('posts/', include('posts.urls')),
    path('messages/', include('messages.urls')),
    
]
