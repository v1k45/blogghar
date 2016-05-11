from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'about', 'user_type', 'last_updated')
    search_fields = ('user', 'about')
