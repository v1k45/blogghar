from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Prefetch

from .models import UserProfile
from comments.models import Comment


class UserProfileView(DetailView):
    template_name = 'authapp/user_profile.html'
    model = UserProfile
    context_object_name = 'profile'
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get_queryset(self):
        queryset = self.model.objects.select_related(
            'user', 'user__blog').prefetch_related('user__posts')
        return queryset


@login_required
def profile_redirector(request):
    return redirect('profile', username=request.user.username)


class UserComments(SingleObjectMixin, ListView):
    template_name = 'authapp/user_profile.html'
    model = UserProfile
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=self.model.objects.select_related(
                'user', 'user__blog').prefetch_related(
                    Prefetch(
                        'user__comments',
                        queryset=Comment.objects.select_related(
                            'post').filter(is_public=True)
                    ),
                    'user__posts')
            )
        return super(UserComments, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserComments, self).get_context_data(**kwargs)
        context['profile'] = self.object
        return context

    def get_queryset(self):
        return self.object.user.comments.all()
