from django import template
from django.utils.safestring import mark_safe

from simplemde.utils import md2html

register = template.Library()


@register.simple_tag
def render_markdown(content):
    return mark_safe(md2html(content))
