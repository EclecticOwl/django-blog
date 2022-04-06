from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from core.models import Profile

class UserToProfileModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='bob',
            password='kjlekjxlKe13i'
        )
    
    def test_one_to_one_rel(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(self.user.id, profile.user.id)
    
    def test_django_sig_username_profile(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(self.user.username, profile.user.username)
    
        


class IndexTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_access_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')