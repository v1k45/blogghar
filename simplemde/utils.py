import bleach
import markdown
from django.conf import settings

SAFE_TAGS = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "b", "i", "strong", "em", "tt",
    "p", "br",
    "span", "div", "blockquote", "code", "hr",
    "ul", "ol", "li", "dd", "dt",
    "table", "thead", "tbody", "tfoot", "tr", "th", "td",
    "img", "a", "abbr", "acronym",
]

SAFE_ATTRS = {
    "*": ["class", "style"],
    "img": ["src", "alt", "title", "width", "height"],
    "a": ["href", "alt", "title", "rel"],
    "abbr": ["title"],
    "acronym": ["title"],
}


def md2html(content):
    cleaned_content = bleach.clean(content, []).replace('&gt;', '>')
    unclean_html = markdown.markdown(
        cleaned_content, extensions=settings.MARKDOWN_EXTENSIONS)
    response = bleach.clean(unclean_html, SAFE_TAGS, SAFE_ATTRS)
    return response
