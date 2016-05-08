from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Blog
from .forms import BlogForm
from .decorators import create_or_edit_blog


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

        return context

    def get_queryset(self):
        return self.object.posts.published()


blog_detail = BlogDetail.as_view()


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
    success_url = '/accounts/profile/'

blog_create = BlogCreateView.as_view()


class BlogUpdateView(BlogModelMixin, UpdateView):
    template_name_suffix = '_update_form'
    success_url = '/accounts/profile/'

    def get_object(self, queryset=None):
        return self.request.user.blog

blog_update = BlogUpdateView.as_view()
