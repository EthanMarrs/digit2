from django.contrib import admin
from core import models, views
from django.http import HttpResponse
from django.conf.urls import url


class DashboardSite(admin.AdminSite):

    def get_urls(self):
        urls = super(DashboardSite, self).get_urls()
        urls += [
            url(r'^dashboard/$', views.DashboardAdminView.as_view())
        ]
        return urls

dashboard_site = DashboardSite()


@admin.register(models.Question, site=dashboard_site)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'explanation', 'state')


@admin.register(models.Syllabus, site=dashboard_site)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'grade')

dashboard_site.register(models.Option)
dashboard_site.register(models.QuestionResponse)
dashboard_site.register(models.Grade)
dashboard_site.register(models.Topic)
dashboard_site.register(models.Block)
dashboard_site.register(models.Subject)
dashboard_site.register(models.QuestionOrder)

