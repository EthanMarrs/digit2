# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-19 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20160912_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionorder',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]
