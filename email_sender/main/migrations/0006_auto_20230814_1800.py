# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2023-08-14 18:00
from __future__ import unicode_literals

from django.db import migrations, models

def populate_track_num(apps, schema_editor):
    SentMessage = apps.get_model('main', 'SentMessage')  # Замените 'main' на имя вашего приложения
    for message in SentMessage.objects.all():
        message.track_num = 2  # Задайте значение по умолчанию
        message.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_sentmessage_track_num'),
    ]

    operations = [

        migrations.AlterField(
            model_name='sentmessage',
            name='track_num',
            field=models.BigIntegerField(blank=True, default=None),
        ),
        migrations.RunPython(populate_track_num),
    ]
