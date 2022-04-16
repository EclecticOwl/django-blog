from django.test import TestCase

from django.contrib.auth.models import User
from core.models import Profile
from usermessaging.models import Message

class TestMessageModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='bob', password='test')
        User.objects.create_user(username='bob2', password='test')

        cls.profile = Profile.objects.get(id=1)
        cls.profile2 = Profile.objects.get(id=2)

        Message.objects.create(
            sender=cls.profile,
            receiver=cls.profile2,
            subject='Test Message',
            content='test',
            is_read=False,)

    def test_details(self):
        message = Message.objects.get(id=1)

        self.assertEqual(message.sender, self.profile)
        self.assertEqual(message.receiver, self.profile2)
        self.assertEqual(message.subject, 'Test Message')
        self.assertEqual(message._meta.get_field('subject').max_length, 100)
        self.assertEqual(message.content, 'test')
        self.assertEqual(message._meta.get_field('content').max_length, 400)
        self.assertEqual(message.is_read, False)
