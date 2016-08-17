from django.contrib import admin
from core import models


admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Option)
admin.site.register(models.Syllabus)
admin.site.register(models.Grade)
admin.site.register(models.Topic)
admin.site.register(models.Block)
admin.site.register(models.Subject)
