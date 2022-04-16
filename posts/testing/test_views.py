from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.messages import get_messages
from core.models import Profile
from posts.models import Post
from posts import views

class AllPostListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='bob', password='test')
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
        request = self.factory.get('/posts/')
        request.user = self.user
        response = views.AllPostListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(reverse('all-posts'))

        # Login Restrict Check
        request.user = AnonymousUser()
        response = views.AllPostListView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        # General Testing
        request.user = self.user
        response = views.AllPostListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'post_list.html')
        # Test pagination and context obj
        self.assertTrue(response.context_data['page_obj'])
        self.assertEqual(len(response.context_data['page_obj']), 4)

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
        # Test pagination and context obj
        self.assertTrue(response.context_data['object_list'])
        self.assertEqual(len(response.context_data['object_list']), 10)

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
        # Test Post
        self.client.login(username='bob', password='test')
        response = self.client.post('/posts/post/update/1/',
            {'description': 'blaa', 'content': 'blaa'})
        
        post = Post.objects.get(id=1)

        self.assertEqual(post.description, 'blaa')
        self.assertEqual(post.content, 'blaa')

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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'post_delete.html')
        # Test delete post
        self.client.login(username='bob', password='test')
        request = self.client.post('/posts/post/delete/1/')
        message = []
        for item in get_messages(request.wsgi_request):
            message.append(str(item))
        self.assertIn('Post Deleted!', message)


        
        




    

        
