from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser as AS
from usermessaging import views
from usermessaging.models import Message
from core.models import Profile

class MessageHomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='bob', password='test')
    
    def test_details(self):
        ### Check url for desired location
        request = self.factory.get('/messages/')
        request.user = self.user
        response = views.MessageHomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        ### Login Restrict Check
        request = self.factory.get(reverse('messages_home'))
        request.user = AS()
        response = views.MessageHomeView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        ### General Testing
        request.user = self.user
        response = views.MessageHomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'messages_home.html')

class MessageInboxViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='bob', password='test')
        self.user2 = User.objects.create_user(username='bob2', password='test')
        profile = Profile.objects.get(id=1)
        profile2 = Profile.objects.get(id=2)

        Message.objects.create(
            sender=profile2,
            receiver=profile,
            subject='Test Message',
            content='hello',
            is_read=False,
        )
        
    def test_details(self):
        ### Check url for desired location
        request = self.factory.get('/messages/inbox/')
        request.user = self.user
        response = views.MessageInboxView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        ### Login Restrict Check
        request = self.factory.get(reverse('message_inbox'))
        request.user = AS()
        response = views.MessageInboxView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        ### General Testing
        request.user = self.user
        response = views.MessageInboxView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'partials/messages_inbox.html')
        ### Test context data and length
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)

class MessageOutboxViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='bob', password='test')
        self.user2 = User.objects.create_user(username='bob2', password='test')
        profile = Profile.objects.get(id=1)
        profile2 = Profile.objects.get(id=2)

        Message.objects.create(
            sender=profile,
            receiver=profile2,
            subject='Test Message',
            content='hello',
            is_read=False,
        )
        
    def test_details(self):
        ### Check url for desired location
        request = self.factory.get('/messages/outbox/')
        request.user = self.user
        response = views.MessageOutboxView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        ### Login Restrict Check
        request = self.factory.get(reverse('message_outbox'))
        request.user = AS()
        response = views.MessageOutboxView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        ### General Testing
        request.user = self.user
        response = views.MessageOutboxView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'partials/messages_outbox.html')
        ### Test context data and length
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)

class MessageInboxDetailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='bob', password='test')
        self.user2 = User.objects.create_user(username='bob2', password='test')
        profile = Profile.objects.get(id=1)
        profile2 = Profile.objects.get(id=2)

        Message.objects.create(
            sender=profile2,
            receiver=profile,
            subject='ii',
            content='iiii',
            is_read=False,
        )
        
    def test_details(self):
        ### Check url for desired location
        request = self.factory.get('/messages/inbox/1/')
        request.user = self.user
        response = views.MessageInboxDetailView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
        ### Login Restrict Check
        request = self.factory.get(reverse('message_detail_inbox', kwargs={'pk': 1}))
        request.user = AS()
        response = views.MessageInboxDetailView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 302)
        ### General Testing
        request.user = self.user
        response = views.MessageInboxDetailView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'partials/user_inbox.html')
        ### Test context data and length
        self.assertIn('message', response.context_data)
        self.assertEqual(str(response.context_data['message']), 'From bob2 to bob')

class MessageOutboxDetailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='bob', password='test')
        self.user2 = User.objects.create_user(username='bob2', password='test')
        profile = Profile.objects.get(id=1)
        profile2 = Profile.objects.get(id=2)

        Message.objects.create(
            sender=profile,
            receiver=profile2,
            subject='ii',
            content='iiii',
            is_read=False,
        )
        
    def test_details(self):
        ### Check url for desired location
        request = self.factory.get('/messages/outbox/1/')
        request.user = self.user
        response = views.MessageOutboxDetailView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
        ### Login Restrict Check
        request = self.factory.get(reverse('message_detail_outbox', kwargs={'pk': 1}))
        request.user = AS()
        response = views.MessageOutboxDetailView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 302)
        ### General Testing
        request.user = self.user
        response = views.MessageOutboxDetailView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'partials/user_outbox.html')
        ### Test context data and length
        self.assertIn('message', response.context_data)
        self.assertEqual(str(response.context_data['message']), 'From bob to bob2')
        
        