from datetime import timezone

from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Post, Comment, Reply


# Create your tests here.
class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='<PASSWORD>')
        self.image = "images/apple.png"
        self.post = Post.objects.create(title='Test title', content='Test content', image=self.image, user=self.user,
                                        createdat=timezone.min, updatedat=timezone.max)
        self.comment = Comment.objects.create(content='Test comment', user=self.user, post=self.post,
                                              createdat=timezone.min, updatedat=timezone.max)

    def test_post_creation(self):
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(self.post.title, 'Test title')
        self.assertEqual(self.post.content, 'Test content')

    def test_post_view(self):
        self.post.get_post_url()
        response = self.client.get(self.post.get_post_url())
        self.assertEqual(response.status_code, 200)

    def test_add_comment(self):
        self.assertEqual(self.post.commentpost.count(), 1)

    def test_add_reply_comment(self):
        Reply.objects.create(content='Test comment', user=self.user, comment=self.comment,
                             createdat=timezone.min, updatedat=timezone.max)
        self.assertEqual(self.comment.replycomment.count(), 1)
