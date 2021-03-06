from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Profile


class UserToProfileModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='bob',
            password='kjlekjxlKe13i'
        )
    
    def test_one_to_one_relationship(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(self.user.id, profile.user.id)
    
    def test_django_sig_username_profile(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(self.user.username, profile.user.username)
    
class TestProfileModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(
            first_name='Bob',
            last_name='Smith',
            email='test@example.com',
        )
        Profile.objects.create(
            first_name='Bob2',
            last_name='Smith2',
            email='test2@example.com',
        )

    def test_first_name_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('first_name').max_length

        self.assertEqual(max_length, 100)
    
    def test_first_name(self):
        profile = Profile.objects.get(id=1)

        self.assertEqual(profile.first_name, 'Bob')
    
    def test_last_name_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)
    
    def test_last_name(self):
        profile = Profile.objects.get(id=1)

        self.assertEqual(profile.last_name, 'Smith')

    def test_email_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('email').max_length

        self.assertEqual(max_length, 300)
    
    def test_email(self):
        profile = Profile.objects.get(id=1)

        self.assertEqual(profile.email, 'test@example.com')
    
    def test_if_profile_follows_and_unfollows_profile(self):
        profile = Profile.objects.get(id=1)
        profile2 = Profile.objects.get(id=2)
        profile.following.add(profile2)

        self.assertIn(profile, profile2.followers.all())

        profile.following.remove(profile2)

        self.assertNotIn(profile, profile2.followers.all())
