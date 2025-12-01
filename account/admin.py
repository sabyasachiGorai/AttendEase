from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):

    # What to show in the admin list page
    list_display = ('id', 'email', 'name', 'role', 'created_at')
    list_filter = ('role',)

    readonly_fields = ('created_at', 'updated_at', 'last_login')

    fieldsets = (
        ('Login Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role', 'gender')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'name')
    ordering = ('id',)
    filter_horizontal = ()  # Removed groups and permissions


admin.site.register(User, UserAdmin)
