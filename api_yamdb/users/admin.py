from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'confirmation_code',
        'role'
    )
    search_fields = ('username',)
    list_editable = ('bio',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'
