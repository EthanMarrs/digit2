# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-18 23:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20161118_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='description',
        ),
    ]