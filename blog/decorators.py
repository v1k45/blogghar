from functools import wraps

from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from .models import Blog


def create_or_edit_blog(view_func):
    """
    The sole purpose of this decorator is to redirect bloggers/readers
    to appropriate view depending upon their origin of request.
    """

    def _create_or_edit_blog_check(request, *args, **kwargs):

        def _response_decider(url_name):
            """
            url_name: url_name to redirect if condition match fails.
            How it works:
                1. Finds current url_name.
                2. checks if it is okay to visit from that url
                3. If okay, goes to the view_func
                4. If not, redirects to appropriate view_func.
            """
            resolved_name = request.resolver_match.url_name
            if resolved_name == url_name:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('blog:' + url_name)

        UserModel = get_user_model()
        user_id = request.user.id
        user = UserModel.objects.select_related().get(pk=user_id)

        # update user instance on request with related objects to save queries.
        request.user = user

        if user.profile.is_blogger():
            # only access to create/edit views when user is a blogger.
            try:
                if user.blog:  # this will be always true
                    # if user already has a blog:
                    # user should only be able to access blog_update view.
                    return _response_decider('blog_update')
            except Blog.DoesNotExist:
                # if user doesnt have a blog,
                # user should only be able to access blog_create view.
                return _response_decider('blog_create')
        else:
            return redirect('blog:user_blog', username=user.username)

    return wraps(view_func)(_create_or_edit_blog_check)


def blogger_required(view_func):
    """
    Only lets bloggers to access the supplied view and redirects readers.
    """
    def _check_blogger_or_reader(request, *args, **kwargs):

        UserModel = get_user_model()
        user_id = request.user.id
        user = UserModel.objects.select_related(
            'profile', 'blog').prefetch_related().get(pk=user_id)

        # update user instance on request with related objects to save queries.
        request.user = user

        if user.profile.is_blogger():
            try:
                if user.blog:
                    return view_func(request, *args, **kwargs)
            except Blog.DoesNotExist:
                return redirect('blog:blog_create')
        else:
            return redirect('blog:user_blog', username=request.user.username)
    return wraps(view_func)(_check_blogger_or_reader)
