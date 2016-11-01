from django.contrib import admin
from core import models, views
from django.http import HttpResponse
from django.conf.urls import url
from ordered_model.admin import OrderedModelAdmin


@admin.register(models.Question)
class QuestionAdmin(OrderedModelAdmin):
    list_display = ('id', 'content', 'explanation', 'state', 'move_up_down_links')


@admin.register(models.Syllabus)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade')


@admin.register(models.Block)
class QuestionAdmin(OrderedModelAdmin):
    list_display = ('id', 'topic', 'move_up_down_links')

admin.site.register(models.Comment)
admin.site.register(models.Option)
admin.site.register(models.QuestionResponse)
admin.site.register(models.Grade)
admin.site.register(models.Topic)
admin.site.register(models.Subject)
admin.site.register(models.QuestionOrder)
admin.site.register(models.Class)

