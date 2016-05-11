import json

from django.views.generic import CreateView
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from .models import Comment
from .forms import CommentForm


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    @method_decorator([login_required, require_POST])
    def dispatch(self, request, *args, **kwargs):
        return super(CommentCreateView, self).dispatch(request, *args, **kwargs)  # noqa

    def get_form_kwargs(self):
        context = super(CommentCreateView, self).get_form_kwargs()
        context['user'] = self.request.user
        return context

    @staticmethod
    def comment_dict(comment):
        return {
            'id': comment.id,
            'name': comment.author.first_name,
            'link': comment.author.profile.get_absolute_url(),
            'comment': comment.comment,
            'created': comment.created,
        }

    def form_valid(self, form):
        instance = form.save()
        ctx = {'success': True, 'msg': "Comment was created successfully."}
        ctx['data'] = self.comment_dict(instance)
        return JsonResponse(ctx)

    def form_invalid(self, form):
        ctx = {'success': False, 'msg': "Failed to post a comment",
               'errors': json.loads(form.errors.as_json())}
        return JsonResponse(ctx)
