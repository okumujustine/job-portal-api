from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('email', 'first_name', 'last_name', 'role')
    list_filter = ('email', 'first_name', 'last_name',
                   'is_active', 'is_staff', 'role')
    ordering = ('-start_date',)
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_verified',
                    'is_active', 'is_staff', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'phone', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'is_active', 'is_staff', 'role')}
         ),
    )


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Profile)
