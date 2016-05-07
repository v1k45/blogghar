from django.test import TestCase
from django.contrib.auth.models import User
from .models import Blog, Post


class BlogPostQuerysetTestCase(TestCase):
    def setUp(self):
        super_user = User.objects.create_superuser(
            username='super_user', email='super@user.com', password='super@pw')

        blog = Blog(title='Sample blog', tag_line='Sample tag line',
                    short_description='Sample description', author=super_user)
        blog.save()

        blog_post = Post(title='Sample post', content='Sample content',
                         author=super_user, blog=blog)
        blog_post.save()

    def test_draft_queryset_works(self):
        # making sure that post is draft
        blog_post = Post.objects.first()
        self.assertEqual(blog_post.status, 'd')

        draft_posts = Post.objects.draft()
        self.assertEqual(draft_posts.count(), 1)

    def test_published_queryset_works(self):
        # making sure that post is draft
        blog_post = Post.objects.first()
        self.assertEqual(blog_post.status, 'd')

        published_posts = Post.objects.published()
        self.assertEqual(published_posts.count(), 0)

        # making post as published
        blog_post = Post.objects.first()
        blog_post.status = 'p'
        blog_post.save()

        published_posts = Post.objects.published()
        self.assertEqual(published_posts.count(), 1)
