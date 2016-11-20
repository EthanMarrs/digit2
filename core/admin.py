from django.contrib import admin
from core import models, views
from django.http import HttpResponse
from django.conf.urls import url
from ordered_model.admin import OrderedModelAdmin
from django.utils.safestring import mark_safe


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    def edit(self, obj):
        return mark_safe('<a href="/questions/{}/edit/" class="go-button">Edit</a>'.format(obj.id))

    list_display = ('id', 'question_content', 'answer_content', 'additional_info_content', 'state', 'edit')


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
    exclude = ('assigned_by',)

    def save_model(self, request, obj, form, change):
        obj.assigned_by = request.user
        obj.save()


@admin.register(models.Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'syllabus')


@admin.register(models.Block)
class BlockAdmin(OrderedModelAdmin):
    list_display = ('id', 'topic')


@admin.register(models.QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'response')


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'correct')




