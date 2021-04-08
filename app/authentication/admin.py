from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django_object_actions import DjangoObjectActions

from .models import User


#
# Filters
#


class EmailFilter(admin.SimpleListFilter):
    title = "Account type"

    parameter_name = 'account_type'

    def lookups(self, request, model_admin):
        return (
            ('sceneid', 'SceneID'),
            ('normal', 'Normal')
        )

    def queryset(self, request, queryset):
        if self.value() == 'sceneid':
            return queryset.filter(email__icontains="@sceneid.")
        if self.value() == "normal":
            return queryset.exclude(email__icontains="@sceneid.")


@admin.register(User)
class UserAdmin(DjangoObjectActions, DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': [('email', 'password')]}),
        ('Scene', {'fields': [('display_name', 'scene_id')]}),
        # ('Personal info', {'fields': [('first_name', 'last_name')]}),
        ('Important dates', {'fields': [('last_login', 'date_joined')]}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'display_name', 'scene_id', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'display_name', 'scene_id')
    ordering = ('email',)

    def get_list_filter(self, request):
        return (EmailFilter,) + self.list_filter
