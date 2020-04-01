# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-12-12 09:10
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit_autosuggest.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('jderobot_kids', '0003_auto_20191108_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodePermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p', models.BooleanField(default=True)),
                ('r', models.BooleanField(default=True)),
                ('w', models.BooleanField(default=True)),
                ('x', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='pack',
            name='exercises',
        ),
        migrations.RenameField(
            model_name='exercise',
            old_name='referee',
            new_name='evaluator',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='real',
        ),
        migrations.RemoveField(
            model_name='user',
            name='exercises',
        ),
        migrations.RemoveField(
            model_name='user',
            name='packs',
        ),
        migrations.AddField(
            model_name='code',
            name='exercises',
            field=models.ManyToManyField(blank=True, to='jderobot_kids.Exercise'),
        ),
        migrations.AddField(
            model_name='code',
            name='expires',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='exercise',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=taggit_autosuggest.managers.TaggableManager(blank=True, help_text='Etiquetas de Grupo Separadas por coma (i.e: grupo1, grupo2, ...)', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Grupos'),
        ),
        migrations.AddField(
            model_name='user',
            name='subscription_expiration',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 12, 10, 10, 48, 954231)),
        ),
        migrations.AlterField(
            model_name='code',
            name='group',
            field=models.CharField(blank=True, help_text='Si no existe, se crear\xe1 uno nuevo.', max_length=200),
        ),
        migrations.RemoveField(
            model_name='code',
            name='packs',
        ),
        migrations.AddField(
            model_name='code',
            name='packs',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='platform',
            field=models.CharField(blank=True, choices=[('gazebo', 'Gazebo'), ('websim', 'WebSim'), ('real', 'Real'), ('real-jupyter', 'Real-Jupyter'), ('theory', 'Theory'), ('vision', 'Vision'), ('tutorials', 'Tutoriales')], max_length=40),
        ),
        migrations.DeleteModel(
            name='Pack',
        ),
        migrations.AddField(
            model_name='codepermissions',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jderobot_kids.Exercise'),
        ),
        migrations.AddField(
            model_name='codepermissions',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
