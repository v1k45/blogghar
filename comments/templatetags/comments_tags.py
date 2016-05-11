from django import template

from comments.forms import CommentForm
from comments.models import Comment

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_comment_form(context, post):
    user = context['user']
    initial = {'post_id': post.id}
    form = CommentForm(user=user, initial=initial)
    return form


@register.assignment_tag
def get_comment_list(post):
    comments = Comment.objects.select_related(
        'author', 'post').filter(post=post).filter(is_public=True)
    return comments
