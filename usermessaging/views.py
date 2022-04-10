from django.shortcuts import render

from .models import Message


def message_inbox(request):
    user = request.user.profile
    inbox = Message.objects.filter(receiver=user)

    context = {'inbox': inbox}
    return render(request, 'messages_inbox.html', context)

def message_outbox(request):
    user = request.user.profile
    outbox = Message.objects.filter(sender=user)

    context = {'outbox': outbox}
    return render(request, 'messages_outbox.html', context)

def message_detail_inbox(request, id):
    message = request.user.profile.receiver.get(id=id)


    context = {'message': message}
    return render(request, 'user_inbox.html', context)

def message_detail_outbox(request, id):
    message = request.user.profile.sender.get(id=id)

    context = {'message': message}
    return render(request, 'user_outbox.html', context)