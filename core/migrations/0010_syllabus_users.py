# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-19 21:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_auto_20160919_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='syllabus',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
