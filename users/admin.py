from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'university_email', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'university_email', 'first_name', 'last_name']
    ordering = ['university_email']

    fieldsets = (
        (None, {'fields': ('university_email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('university_email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Profile)