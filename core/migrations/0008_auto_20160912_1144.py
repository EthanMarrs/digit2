# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-12 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160912_1110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='block',
            options={'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='block',
            name='order',
            field=models.PositiveIntegerField(db_index=True, editable=False),
        ),
    ]
