from django.contrib import admin
from .models import Blog, Post, Tag


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag_line', 'author',
                    'created', 'is_public', 'is_deleted')
    search_fields = ('title', 'tag_line', 'short_description')
    list_filter = ('is_public', 'is_deleted')
    readonly_fields = ('created', 'last_modified')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog', 'author', 'is_published', 'created')
    search_fields = ('title', 'summary', 'content')
    list_filter = ('status', 'created')
    readonly_fields = ('created', 'last_modified')

    fieldsets = (
        (None, {'fields': ('title', 'slug', 'summary', 'content', 'tags')}),
        ('Other details', {'fields': ('status', 'blog', 'author')}),
        ('Dates', {'fields': ('created', 'last_modified')}),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = list_display
