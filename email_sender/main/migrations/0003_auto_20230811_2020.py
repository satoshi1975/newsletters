# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2023-08-11 20:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_subsriber_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subsriber',
            new_name='Subscriber',
        ),
    ]