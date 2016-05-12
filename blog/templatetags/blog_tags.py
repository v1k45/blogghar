from django import template

register = template.Library()


@register.assignment_tag
def latest_post(user, limit=5):
    qs = user.posts.published()[:limit]
    return qs
