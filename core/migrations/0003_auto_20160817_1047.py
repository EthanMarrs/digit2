# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-17 10:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160817_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Block'),
        ),
    ]
