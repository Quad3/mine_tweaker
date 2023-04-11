from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from datetime import datetime

from .models import Post, Comment
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


class HomePageTests(TestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'tweaker/posts.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Posts')

    def test_homepage_does_not_contains_incorrect_html(self):
        self.assertNotContains(self.response, 'Random string')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )


class CommentTests(TestCase):

    def test_create_comment(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser3',
            email='test@test.com',
            password='testpass',
        )
        post = Post.objects.create(
            text='Comment test post',
            owner=user,
        )
        comment = Comment.objects.create(
            text='first comment',
            post=post,
            owner=user,
        )

        self.assertEqual(len(Comment.objects.all()), 1)
        self.assertEqual(comment.text, 'first comment')
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.owner, user)
        self.assertFalse(comment.likes.all())
