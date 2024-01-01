from django.contrib import admin
from .models import AccountGroup, Group, RandomQuestion, StudentAnswer
from import_export.admin import ImportExportModelAdmin


class GroupAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'course', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['is_active']
    search_fields = ['name', 'course__title']


class AccountGroupAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'group', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    list_filter = ['is_active']
    search_fields = ['student__first_name', 'student__last_name', 'group__name']


class RandomQuestionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'status', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    list_filter = ['status']
    search_fields = ['student__first_name', 'student__last_name']


class StudentAnswerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'student', 'question', 'answer', 'is_correct', 'created_at', 'updated_at']
    list_display_links = ['id', 'student']
    list_filter = ['is_correct']
    search_fields = ['student__first_name', 'student__last_name', 'question__question', 'answer__answer']



admin.site.register(StudentAnswer, StudentAnswerAdmin)
admin.site.register(RandomQuestion, RandomQuestionAdmin)
admin.site.register(AccountGroup, AccountGroupAdmin)
admin.site.register(Group, GroupAdmin)
