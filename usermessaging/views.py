from django.shortcuts import render

from .models import Message


def message_list(request):
    user = request.user.profile
    inbox = Message.objects.filter(receiver=user)

    context = {'inbox': inbox}
    return render(request, 'messages.html', context)