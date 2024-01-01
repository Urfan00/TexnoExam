from django.contrib import admin
from .models import Answer, Course, CourseTopic, Question
from import_export.admin import ImportExportModelAdmin


class CourseAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title']


class CourseTopicAdmin(ImportExportModelAdmin):
    list_display = ['id', 'topic_title', 'course', 'created_at', 'updated_at']
    list_display_links = ['id', 'topic_title']
    search_fields = ['topic_title', 'course__title']


class QuestionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'question' ,'point' ,'course_topic', 'question_image', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'question']
    list_filter = ['point', 'is_active']
    search_fields = ['question', 'course_topic__topic_title']


class AnswerAdmin(ImportExportModelAdmin):
    list_display = ['id', 'answer', 'question', 'is_correct', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'answer']
    list_filter = ['is_correct', 'is_active']
    search_fields = ['answer', 'question__question']


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseTopic, CourseTopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
