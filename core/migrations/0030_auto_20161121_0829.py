# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-21 08:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_merge_20161121_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='week_start',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
