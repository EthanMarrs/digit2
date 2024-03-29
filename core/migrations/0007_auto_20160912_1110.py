# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-12 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionorder',
            name='open',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
