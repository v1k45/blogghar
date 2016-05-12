import uuid

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Prefetch

from .models import UserProfile
from comments.models import Comment
from .forms import UserForm, UserProfileForm


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
    return redirect('authapp:profile', username=request.user.username)


class UserComments(SingleObjectMixin, ListView):
    template_name = 'authapp/user_comments.html'
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
        context['comments'] = self.get_queryset()
        return context

    def get_queryset(self):
        qs = self.object.user.comments.all()
        return qs


class UserProfileUpdateView(UpdateView):

    template_name = 'authapp/edit_profile.html'
    form_class = UserForm
    form_class_2 = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.request.user)
        if 'form2' not in context:
            context['form2'] = self.form_class_2(instance=self.request.user.profile)  # noqa
        return context

    def get(self, request, *args, **kwargs):
        super(UserProfileUpdateView, self).get(request, *args, **kwargs)
        self.object = self.get_object()
        form = self.form_class(instance=self.request.user)
        form2 = self.form_class_2(instance=self.request.user.profile)

        return self.render_to_response(self.get_context_data(
            form=form, form2=form2
        ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.request.user)
        form2 = self.form_class_2(request.POST, request.FILES,
                                  instance=self.request.user.profile)

        if form.is_valid() and form2.is_valid():
            form.save()
            data = form2.save(commit=False)
            if request.FILES.get('avatar', None):
                data.avatar = request.FILES['avatar']
                data.avatar.name = '{0}_p.jpg'.format(str(uuid.uuid4()))
            data.save()
            return redirect('authapp:user_profile')
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2)
                )

    def get_object(self, queryset=None):
        return self.request.user
