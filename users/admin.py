from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'username', 'email', 'bio', 'role',
    )
    search_fields = ('username',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'
