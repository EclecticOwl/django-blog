from django.forms import ModelForm

from .models import Message

class CustomMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content']
