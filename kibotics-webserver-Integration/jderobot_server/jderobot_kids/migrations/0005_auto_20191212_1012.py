# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-12-12 09:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('jderobot_kids', '0004_auto_20191212_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='packs',
        ),
        migrations.AddField(
            model_name='code',
            name='packs',
            field=models.ManyToManyField(blank=True, to='taggit.Tag'),
        ),
        migrations.AlterField(
            model_name='user',
            name='subscription_expiration',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 12, 10, 12, 33, 838426)),
        ),
    ]
