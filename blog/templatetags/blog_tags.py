from django import template
from django.db.models import Count

register = template.Library()


@register.assignment_tag
def latest_post(user, limit=5):
    qs = user.posts.published().annotate(
        comment_count=Count('comments')).filter(blog__is_public=True)[:limit]
    return qs
