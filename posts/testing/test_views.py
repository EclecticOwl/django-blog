from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from core.models import Profile
from posts.models import Post

class AllPostListTest(TestCase):
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
    def test_if_redirect_if_anon(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
    
    def test_url_access_by_name(self):
        self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get(reverse('all-posts'))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template(self):
        self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get(reverse('all-posts'))
        self.assertTemplateUsed(response, 'post_list.html')
    
    def test_if_correct_num_posts_displayed(self):
        self.client.login(username='bob', password='kjlekjxlKe13i')
        response = self.client.get(reverse('all-posts'))
        self.assertTrue(response.context['page_obj'])
        self.assertEqual(len(response.context['page_obj']), 4)
