from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'short_comment', 'post',
                    'is_public', 'is_removed', 'created')
    list_filter = ('post', 'is_public', 'is_removed')
    search_fields = ('comment', 'post', 'author')

    def short_comment(self, obj):
        return truncatechars(obj.comment, 100)
