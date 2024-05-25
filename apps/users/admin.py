from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'username', 'is_staff', 'is_email_verified', 'role',
    )
    list_filter = ('is_staff', 'is_email_verified', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': (
            'is_staff', 'is_active', 'is_email_verified', 'role'
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password1', 'password2', 'is_staff',
                'is_active', 'is_email_verified', 'role'
            )}),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
