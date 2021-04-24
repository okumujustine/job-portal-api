from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework_simplejwt import token_blacklist

from .models import CustomUser, Profile


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True  # or whatever logic you want


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
admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken,
                    OutstandingTokenAdmin)
