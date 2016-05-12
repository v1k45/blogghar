from ddt import ddt, data as ddt_data, unpack

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import Blog, Post, Tag
from comments.models import Comment
from .test_utils import annotate_dict, initial_users, auth_ddt_data


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


@ddt
class BlogDetailViewTestCase(TestCase):

    def setUp(self):
        """
        Initial tests data for individual testcases.
        """
        users = initial_users()
        for user_type, user_instance in users.items():
            setattr(self, user_type, user_instance)

    @unpack
    @ddt_data(
        annotate_dict({'user': 'user_with_blog', 'has_blog': True}, 'user'),
        annotate_dict({'user': 'user_without_blog', 'has_blog': False}, 'user'),
        annotate_dict({'user': 'reader_without_blog', 'has_blog': False}, 'user'))
    def test_blog_detail_view_is_accessible(self, user, has_blog):
        target = reverse('blog:user_blog', args=[user])
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        requested_user = User.objects.get(username=user)
        self.assertEqual(response.context['requested_user'], requested_user)
        self.assertEqual(response.context['posts'].count(), 0)

        if has_blog:
            self.assertTrue(response.context['has_blog'])
            self.assertEqual(response.context['blog'], requested_user.blog)
        else:
            self.assertFalse(response.context['has_blog'])


class PostDetailViewTestCase(TestCase):

    def setUp(self):
        """
        Initial tests data for individual testcases.
        """
        users = initial_users()
        for user_type, user_instance in users.items():
            setattr(self, user_type, user_instance)

    def test_post_detail_is_accessible(self):
        blog_post = Post(title='Sample post', content='Sample content',
                         author=self.user_with_blog, status='p',
                         blog=self.user_with_blog.blog)
        blog_post.save()

        target = reverse('blog:post_detail',
                         args=[self.user_with_blog.username, blog_post.slug])
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertEqual(response.context['post'], blog_post)


class TagggedPostsListViewTestCase(TestCase):

    def setUp(self):
        """
        Initial tests data for individual testcases.
        """
        users = initial_users()
        for user_type, user_instance in users.items():
            setattr(self, user_type, user_instance)

    def test_tag_posts_list_view_is_accessible(self):
        blog_post = Post(title='Sample post', content='Sample content',
                         author=self.user_with_blog, status='p',
                         blog=self.user_with_blog.blog)
        blog_post.save()

        tag = Tag.objects.create(name='sample')

        blog_post.tags.add(tag)

        self.assertTrue(Post.objects.filter(tags__slug=tag.slug).exists())

        target = reverse('blog:tagged_posts_list', args=[tag.slug])
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/tagged_posts_list.html')
        self.assertEqual(response.context['posts'].count(), 1)


@ddt
class BlogCreateViewTestCase(TestCase):
    def setUp(self):
        """
        Initial tests data for individual testcases.
        """
        users = initial_users()
        for user_type, user_instance in users.items():
            setattr(self, user_type, user_instance)

    @unpack
    @ddt_data(auth_ddt_data('user_without_blog', 'user_without_blog@pw'))
    def test_blog_create_is_accessible_to(self, username, password):
        self.assertTrue(
            self.client.login(username=username, password=password))
        target = reverse('blog:blog_create')
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_create_form.html')

    @unpack
    @ddt_data(
        auth_ddt_data('reader_without_blog', 'reader_without_blog@pw'),
        auth_ddt_data('user_with_blog', 'user_with_blog@pw'),)
    def test_blog_create_is_not_accessible_to(self, username, password):
        self.assertTrue(
            self.client.login(username=username, password=password))
        target = reverse('blog:blog_create')
        response = self.client.get(target)
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'blog/blog_create_form.html')

    @unpack
    @ddt_data(auth_ddt_data('user_without_blog', 'user_without_blog@pw'))
    def test_blog_create_post_request(self, username, password):
        self.assertTrue(
            self.client.login(username=username, password=password))

        data = {
            'title': 'Sample blog',
            'tag_line': 'Sample blog',
            'short_description': 'Sample Blog',
            'is_public': True
        }

        target = reverse('blog:blog_create')
        response = self.client.post(target, data)
        self.assertRedirects(response, reverse('authapp:user_profile'),
                             target_status_code=302)

        self.assertTrue(Blog.objects.filter(author__username=username).exists())


class BlogUpdateViewTestCase(TestCase):
    def setUp(self):
        """
        Initial tests data for individual testcases.
        """
        users = initial_users()
        for user_type, user_instance in users.items():
            setattr(self, user_type, user_instance)

    def test_blog_update_is_accessible_via_get(self):
        self.assertTrue(
            self.client.login(username='user_with_blog',
                              password='user_with_blog@pw'))
        target = reverse('blog:blog_update')
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_update_form.html')

    def test_blog_update_post_request(self):
        self.assertTrue(
            self.client.login(username='user_with_blog',
                              password='user_with_blog@pw'))
        data = {
            'title': 'Edited Sample blog',
            'tag_line': 'Edited tag_line',
            'short_description': 'Sample Blog',
            'is_public': True
        }

        target = reverse('blog:blog_update')
        response = self.client.post(target, data)
        self.assertRedirects(response, reverse('authapp:user_profile'),
                             target_status_code=302)

        updated_blog = Blog.objects.first()
        self.assertEqual(updated_blog.title, data['title'])


class PostCreateViewTestCase(TestCase):
    def setUp(self):
        """
        Initial tests data for individual testcases.
        """
        users = initial_users()
        for user_type, user_instance in users.items():
            setattr(self, user_type, user_instance)

    def test_post_create_is_accessible_via_get(self):
        self.assertTrue(
            self.client.login(username='user_with_blog',
                              password='user_with_blog@pw'))
        target = reverse('blog:post_create')
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_create_form.html')

    def test_blog_create_post_request(self):
        self.assertTrue(
            self.client.login(username='user_with_blog',
                              password='user_with_blog@pw'))

        data = {
            'title': 'Sample blog',
            'slug': 'sample-blog',
            'content': 'Sample Blog',
            'summary': 'sample',
            'tags': [],
        }

        target = reverse('blog:post_create')
        response = self.client.post(target, data)
        self.assertRedirects(response, reverse('blog:user_posts'))

        self.assertTrue(
            Post.objects.filter(author__username='user_with_blog').exists())


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        """
        Initial tests data for individual testcases.
        """
        users = initial_users()
        for user_type, user_instance in users.items():
            setattr(self, user_type, user_instance)

        blog_post = Post(title='Sample post', content='Sample content',
                         author=self.user_with_blog,
                         blog=self.user_with_blog.blog)
        blog_post.save()
        self.blog_post = Post.objects.first()

    def test_post_update_is_accessible_via_get(self):
        self.assertTrue(
            self.client.login(username='user_with_blog',
                              password='user_with_blog@pw'))
        target = reverse('blog:post_update', args=[self.blog_post.slug])
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_update_form.html')

    def test_post_update_post_request(self):
        self.assertTrue(
            self.client.login(username='user_with_blog',
                              password='user_with_blog@pw'))

        data = {
            'title': 'Edited post',
            'slug': self.blog_post.slug,
            'content': 'Sample Blog',
            'summary': 'sample',
            'tags': [],
        }

        target = reverse('blog:post_update', args=[self.blog_post.slug])
        response = self.client.post(target, data)
        self.assertRedirects(response, reverse('blog:user_posts'))

        updated_post = Post.objects.first()
        self.assertEqual(updated_post.title, data['title'])


class UserPostsListViewTestCase(TestCase):

    def setUp(self):
        """
        Initial tests data for individual testcases.
        """
        users = initial_users()
        for user_type, user_instance in users.items():
            setattr(self, user_type, user_instance)

    def test_user_posts_list_view_is_accessible(self):
        blog_post = Post(title='Sample post', content='Sample content',
                         author=self.user_with_blog, status='p',
                         blog=self.user_with_blog.blog)
        blog_post.save()
        self.assertTrue(
            self.client.login(username='user_with_blog',
                              password='user_with_blog@pw'))
        target = reverse('blog:user_posts')
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/user_posts.html')
        self.assertEqual(response.context['posts'].count(), 1)


@ddt
class BlogCommentsViewTestCase(TestCase):

    def setUp(self):
        """
        Initial tests data for individual testcases.
        """
        users = initial_users()
        for user_type, user_instance in users.items():
            setattr(self, user_type, user_instance)

    @unpack
    @ddt_data({'comment': False}, {'comment': True})
    def test_blog_comments_view_comment(self, comment):
        blog_post = Post(title='Sample post', content='Sample content',
                         author=self.user_with_blog, status='p',
                         blog=self.user_with_blog.blog)
        blog_post.save()
        if comment:
            comment = Comment(author=self.user_with_blog, post=blog_post,
                              comment='test comment')
            comment.save()
            comment_count = 1
        else:
            comment_count = 0

        self.assertTrue(
            self.client.login(username='user_with_blog',
                              password='user_with_blog@pw'))

        target = reverse('blog:blog_comments')
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comments_list.html')
        self.assertEqual(response.context['comments'].count(), comment_count)
