from django.contrib import admin

from backend.foodgram import settings
from backend.users.models import CustomUser, Follow


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'password',
        'first_name',
        'last_name',
        'email'
    )
    list_filter = (
        'username',
        'email'
    )
    search_fields = (
        'username',
        'email'
    )
    empty_value_display = settings.EMPTY


class FollowsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    list_filter = (
        'user',
        'author'
    )
    search_fields = (
        'user',
        'author'
    )
    empty_value_display = settings.EMPTY


admin.site.register(CustomUser, UsersAdmin)
admin.site.register(Follow, FollowsAdmin)
