from django.contrib.auth import get_user_model
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DetailView, DeleteView)
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Count, Prefetch
from django.core.urlresolvers import reverse_lazy

from dal import autocomplete

from .models import Blog, Post, Tag
from .forms import BlogForm, PostForm
from .decorators import create_or_edit_blog, blogger_required
from comments.models import Comment


class BlogDetail(SingleObjectMixin, ListView):
    template_name = 'blog/blog_detail.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'requested_user'

    def get(self, request, *args, **kwargs):
        UserModel = get_user_model()
        self.object = self.get_object(
            queryset=UserModel.objects.select_related().prefetch_related('blog__posts')  # noqa
        )
        return super(BlogDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        context['requested_user'] = self.object

        try:
            context['blog'] = self.object.blog
            context['has_blog'] = True
        except Blog.DoesNotExist:
            context['has_blog'] = False

        context['posts'] = self.get_queryset()

        return context

    def get_queryset(self):
        return self.object.posts.published().annotate(comment_count=Count('comments'))   # noqa


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        queryset = Post.objects.published().select_related(
            'author', 'blog', 'author__profile').prefetch_related(
                Prefetch('comments',
                         queryset=Comment.objects.select_related(
                             'author', 'author__profile',
                             'post', 'post__author').filter(is_public=True))
            ).filter(
                author__username=self.kwargs['username'])
        return queryset


class TagggedPostsList(ListView):
    model = Post
    template_name = 'blog/tagged_posts_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(TagggedPostsList, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context

    def get_queryset(self):
        queryset = Post.objects.published().select_related(
            'author', 'blog', 'author__profile').prefetch_related(
                'tags').annotate(
                    comment_count=Count('comments')).filter(
                        tags__slug=self.kwargs['tag'], blog__is_public=True)
        return queryset


class BlogModelMixin(object):
    model = Blog
    form_class = BlogForm

    @method_decorator([login_required, create_or_edit_blog])
    def dispatch(self, request, *args, **kwargs):
        return super(BlogModelMixin, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(BlogModelMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BlogCreateView(BlogModelMixin, CreateView):
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('authapp:user_profile')


class BlogUpdateView(BlogModelMixin, UpdateView):
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('authapp:user_profile')

    def get_object(self, queryset=None):
        return self.request.user.blog


class PostModelMixin(object):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:user_posts')

    @method_decorator([login_required, blogger_required])
    def dispatch(self, request, *args, **kwargs):
        return super(PostModelMixin, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostModelMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        form.save_m2m()
        return redirect(self.success_url)


class PostCreateView(PostModelMixin, CreateView):
    template_name_suffix = '_create_form'


class PostUpdateView(PostModelMixin, UpdateView):
    template_name_suffix = '_update_form'

    def get_queryset(self):
        return self.request.user.posts.all()


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:user_posts')
    template_name_suffix = '_delete_form'

    @method_decorator([login_required, blogger_required])
    def dispatch(self, request, *args, **kwargs):
        return super(PostDeleteView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.request.user.posts.all()
        return qs


class TagAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    @method_decorator([login_required, blogger_required])
    def dispatch(self, request, *args, **kwargs):
        return super(TagAutoComplete, self).dispatch(request, *args, **kwargs)

tag_autocomplete = TagAutoComplete.as_view()


class UserPostsList(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'

    @method_decorator([login_required, blogger_required])
    def dispatch(self, request, *args, **kwargs):
        return super(UserPostsList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Post.objects.select_related(
            'author', 'blog').prefetch_related('tags').filter(author=self.request.user)  # noqa
        return queryset


class BlogComments(ListView):
    model = Comment
    template_name = 'blog/comments_list.html'
    context_object_name = 'comments'

    @method_decorator([login_required, blogger_required])
    def dispatch(self, request, *args, **kwargs):
        return super(BlogComments, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.select_related(
            'post', 'post__blog').filter(post__blog=self.request.user.blog)
        return queryset


class HomeTemplateView(ListView):
    template_name = 'blog/home.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.published().select_related(
            'author', 'author__profile', 'blog').prefetch_related(
                'tags').annotate(comment_count=Count('comments')).filter(blog__is_public=True)  # noqa
        return queryset
