from django.test import TestCase

from core.models import Profile
from posts.models import Post


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(
            username='bob',
            first_name='Bob',
            last_name='Smith',
            email='test@example.com',
        )
        cls.profile = Profile.objects.get(id=1)
        Post.objects.create(
            owner=cls.profile,
            description='hello',
            content='hello world',
        )
    
    def test_post_owner(self):
        post = Post.objects.get(id=1)
        self.assertEqual(str(post.owner), 'bob')
    
    def test_description_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('description').max_length
        self.assertEqual(max_length, 100)
    
    def test_content_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('content').max_length
        self.assertEqual(max_length, 400)
    

