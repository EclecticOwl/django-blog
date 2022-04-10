from django.shortcuts import render

from .models import Message


def message_list(request):
    user = request.user.profile
    inbox = Message.objects.filter(receiver=user)

    context = {'inbox': inbox}
    return render(request, 'messages.html', context)

def message_detail(request, id):
    message = request.user.profile.receiver.get(id=id)


    context = {'message': message}
    return render(request, 'user_message.html', context)