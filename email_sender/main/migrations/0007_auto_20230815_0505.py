# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2023-08-15 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20230814_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentmessage',
            name='message',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='sentmessage',
            name='status',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
