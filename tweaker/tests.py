from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from datetime import datetime

from .models import Post
from .views import HomePageView


class PostTests(TestCase):

    def test_create_post(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass',
        )
        user2 = User.objects.create_user(
            username='testuser2',
            email='test@test.com',
            password='testpass',
        )
        post = Post.objects.create(
            text='some text.',
            owner=user,
        )
        post.postlike_set.create(
            user=user,
        )
        post.postlike_set.create(
            user=user2,
        )

        self.assertEqual(post.text, 'some text.')
        self.assertEqual(post.owner, user)
        self.assertEqual(post.created_at, post.modified_at)
        self.assertLessEqual((datetime.utcnow() - post.created_at).seconds, 2)
        self.assertEqual(post.postlike_set.first().user, user)
        self.assertEqual(len(post.postlike_set.get_queryset()), 2)


class HomePageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_homepage_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'tweaker/home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Home')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )
