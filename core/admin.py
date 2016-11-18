from django.contrib import admin
from core import models, views
from django.http import HttpResponse
from django.conf.urls import url
from ordered_model.admin import OrderedModelAdmin


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_content', 'answer_content', 'additional_info_content', 'state')


@admin.register(models.Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade')


@admin.register(models.Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'syllabus', 'week_start', 'duration')


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'assigned_by', 'assigned_to', 'topic', 'open', 'due_date')


@admin.register(models.Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'syllabus')


admin.site.register(models.Option)
admin.site.register(models.QuestionResponse)
admin.site.register(models.Subject)


