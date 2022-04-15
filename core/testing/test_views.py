from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Profile
from posts.models import Post


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

class UserProfilePageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='bob',
            password='kjlekjxlKe13i'
        )
        cls.user.set_password('kjlekjxlKe13i')
        cls.user.save()
    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_access_by_name(self):
        login = self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        login = self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get(reverse('user-profile'))
        self.assertTemplateUsed('profile.html')
        
class EditUserProfilePageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='bob',
            password='kjlekjxlKe13i'
        )
        cls.user.set_password('kjlekjxlKe13i')
        cls.user.save()

    
    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get('/account/edit/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_access_by_name(self):
        login = self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get(reverse('update-user-profile', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        login = self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get(reverse('update-user-profile', kwargs={'pk': 1}))
        self.assertTemplateUsed('edit_profile.html')
    
    def test_update_profile_information(self):
        login = self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.post('/account/edit/1/', 
            {'first_name': 'bob', 'last_name': 'smith', 'email': 'bob@example.com'})

        profile = Profile.objects.get(id=1)

        self.assertEqual(profile.first_name, 'bob')
        self.assertEqual(profile.last_name, 'smith')
        self.assertEqual(profile.email, 'bob@example.com')
        

