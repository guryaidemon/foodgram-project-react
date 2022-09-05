from django.contrib import admin

from foodgram import settings
from users.models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Представляет модель User в интерфейсе администратора."""
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'password'
    )
    list_filter = ('email', 'username', )
    empty_value_display = settings.EMPTY


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Представляет модель Follow в интерфейсе администратора."""
    list_display = ('id', 'user', 'author')
    search_fields = ('user',)
    list_filter = ('user', )
    empty_value_display = settings.EMPTY
