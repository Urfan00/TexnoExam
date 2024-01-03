from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account, StudentResult
from import_export.admin import ImportExportModelAdmin



class AccountAdmin(ImportExportModelAdmin, BaseUserAdmin):
    list_display = ("username", "first_name", "last_name", 'FIN', "email", "number", "image", "birthday", 'status', 'first_time_login', 'is_delete', "is_active", "is_superuser")
    list_filter = ("is_active", 'is_staff', 'status', 'is_delete', "is_superuser", 'first_time_login')
    fieldsets = (
        ("Credential", {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'number', 'image', 'birthday', 'status', 'first_time_login', 'is_delete')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            'CREATE NEW USER',
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "first_name", "last_name", 'FIN', "email", "number"),
            },
        ),
    )
    search_fields = ("username", "first_name", "last_name", 'FIN', "email", "number")


class StudentResultAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'point_1', 'point_2', 'point_3', 'total_point', 'status', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    search_fields = ['student__first_name', 'student__last_name', 'student__email']
    list_filter = ['status']


admin.site.register(Account, AccountAdmin)
admin.site.register(StudentResult, StudentResultAdmin)
