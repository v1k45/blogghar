from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from .models import UserProfile


class UserProfile(DetailView):
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
