from django.contrib.auth import get_user_model
from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin

from .models import Blog


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
