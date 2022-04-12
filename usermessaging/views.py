from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


from .models import Message
from core.models import Profile

from .forms import CustomMessageForm


class MessageHomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'messages_home.html'


class MessageInboxView(LoginRequiredMixin, generic.ListView):
    template_name = 'partials/messages_inbox.html'
    model = Message

    def get_queryset(self):
        queryset = Message.objects.filter(receiver=self.request.user.profile)
        return queryset

class MessageOutboxView(LoginRequiredMixin, generic.ListView):
    template_name = 'partials/messages_outbox.html'
    model = Message

    def get_queryset(self):
        queryset = Message.objects.filter(receiver=self.request.user.profile)
        return queryset



def message_detail_inbox(request, id):
    message = request.user.profile.receiver.get(id=id)


    context = {'message': message}
    return render(request, 'partials/user_inbox.html', context)


def message_detail_outbox(request, id):
    message = request.user.profile.sender.get(id=id)

    context = {'message': message}
    return render(request, 'partials/user_outbox.html', context)



def send_message(request, id):
    recipient = Profile.objects.get(id=id)
    form = CustomMessageForm()

    if request.method == 'POST':
        form = CustomMessageForm(request.POST)
        if form.is_valid():
            user_message = form.save(commit=False)
            user_message.receiver = recipient
            user_message.sender = request.user.profile
            form.save()
            messages.success(request, 'Your message has been sent.')
            return redirect('index')

        else:
            messages.error(request, 'It appears some of the fields are incorrect or not filled in correctly. Please check and try again.')


    context = {'recipient': recipient, 'form': form}
    return render(request, 'send_message.html', context)