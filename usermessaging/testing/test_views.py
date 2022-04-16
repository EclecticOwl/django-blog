from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser as AS
from usermessaging import views


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