from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from core.models import Profile
from posts.models import Post


######## Model Testing ########

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


######## View Testing ########

class IndexPageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username='bob',
            password='kjlekjxlKe13i'
        )
        User.objects.create(
            username='bob2',
            password='kjlekjxlJJJJJ'
        )

        user = User.objects.get(id=1)
        user.set_password('kjlekjxlKe13i')
        user.save()

        profile = Profile.objects.get(id=1)
        profile2 = Profile.objects.get(id=2)

        profile.following.add(profile2)

        num_posts = 10

        for i in range(num_posts):
            Post.objects.create(
                owner=profile2,
                description=f'{i}',
                content=f'{i}',
            )
        

    ### General Testing ###
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_access_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_if_correct_num_posts_displayed(self):
        self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get(reverse('index'))

        self.assertTrue(response.context['profile_feed'])
        self.assertEqual(len(response.context['profile_feed']), 10)

    def test_if_profile_feed_displays_for_anonymous(self):
        response = self.client.get(reverse('index'))

        self.assertFalse('profile_feed' in response.context)

class RegisterPageTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_access_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'register.html')
    
class LoginPageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='bob',
            password='kjlekjxlKe13i'
        )
        cls.user.set_password('kjlekjxlKe13i')
        cls.user.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/sign-in/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_access_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_successful(self):
        response = self.client.post('/sign-in/', 
            {'username': 'bob', 'password': 'kjlekjxlKe13i'})

        self.assertEqual(response.status_code, 302)

    def test_login_unsuccessful(self):
        response = self.client.post('/sign-in/', 
            {'username': 'bob', 'password': 'kjjfjdka'})
        check_user_type = response.context['user']

        self.assertTrue(str(check_user_type) == 'AnonymousUser')









        
        




