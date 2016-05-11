from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from blog.models import Blog, Post
from .models import Comment
from authapp.models import UserProfile


class CommentViewTestCase(TestCase):
    def setUp(self):
        super_user = User.objects.create_superuser(
            username='super_user', email='super@user.com', password='super@pw')

        profile = UserProfile(user=super_user)
        profile.save()

        blog = Blog(title='Sample blog', tag_line='Sample tag line',
                    short_description='Sample description', author=super_user)
        blog.save()

        blog_post = Post(title='Sample post', content='Sample content',
                         author=super_user, blog=blog, status='p')
        blog_post.save()

    def test_post_comment(self):
        target = reverse('comments:post')
        self.assertTrue(
            self.client.login(username='super_user', password='super@pw')
            )
        data = {
            'comment': "Sample comment",
            'post_id': Post.objects.first().pk
        }
        response = self.client.post(target, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'true')

        self.assertTrue(Comment.objects.exists())
