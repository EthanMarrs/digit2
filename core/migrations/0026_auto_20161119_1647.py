# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-19 16:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_remove_task_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer_content_json',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='question',
            name='question_content_json',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='option',
            name='question',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='core.Question'),
        ),
    ]
