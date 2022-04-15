from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser

from core.models import Profile
from posts.models import Post

from posts import views


class AllPostListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username='bob',
        )
        User.objects.create(
            username='bob2',
            password='kjlekjxlJJJJJ'
        )

        user = User.objects.get(id=1)
        user.set_password('kjlekjxlKe13i')
        user.save()

        cls.user = 'bob'
        cls.password = 'kjlekjxlKe13i'

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
    def test_if_redirect_if_anon(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username=self.user, password=self.password)
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
    
    def test_url_access_by_name(self):
        self.client.login(username=self.user, password=self.password)
        response = self.client.get(reverse('all-posts'))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        self.client.login(username=self.user, password=self.password)
        response = self.client.get(reverse('all-posts'))
        self.assertTemplateUsed(response, 'post_list.html')
    
    def test_if_correct_num_posts_displayed(self):
        self.client.login(username=self.user, password=self.password)
        response = self.client.get(reverse('all-posts'))
        self.assertTrue(response.context['page_obj'])
        self.assertEqual(len(response.context['page_obj']), 4)

class MyPostListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='bob', password='test'
        )
        profile = Profile.objects.get(id=1)

        num_posts = 10

        for i in range(num_posts):
            Post.objects.create(
                owner=profile,
                description=f'{i}',
                content=f'{i}',
            )
    def test_details(self):
        # Check url for desired location
        request = self.factory.get('/posts/my-posts/')
        request.user = self.user
        response = views.MyPostListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(reverse('my-posts'))
        # Login Restrict Check
        request.user = AnonymousUser()
        response = views.MyPostListView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        # General Testing
        request.user = self.user
        response = views.MyPostListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'my_posts.html')

        


class PostUpdateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='bob', password='test'
        )
        profile = Profile.objects.get(id=1)
        Post.objects.create(owner=profile, description='test', content='test')

    def test_details(self):
        # Check url for desired location
        request = self.factory.get('/posts/post/update/1/')
        request.user = self.user
        response = views.PostUpdateView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
        
        request = self.factory.get(reverse('post-update', kwargs={'pk': 1}))
        # Login Restrict Check
        request.user = AnonymousUser()
        response = views.PostUpdateView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 302)
        # General Testing
        request.user = self.user
        response = views.PostUpdateView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'post_update.html')



class PostDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='bob', password='test'
        )
        profile = Profile.objects.get(id=1)
        Post.objects.create(owner=profile, description='test', content='test')
    
    def test_details(self):
        # Check url for desired url location
        request = self.factory.get('/posts/post/delete/1/')
        request.user = self.user
        response = views.PostDeleteView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(reverse('post-delete', kwargs={'pk': 1}))
        # Login Restrict Check
        request.user = AnonymousUser()
        response = views.PostDeleteView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 302)
        # General Testing
        request.user = self.user
        response = views.PostDeleteView.as_view()(request, pk=1)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'post_delete.html')
        
        




    

        
