# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taskmaster_app', '0004_auto_20150208_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default=b'slug_placeholder', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='slug',
            field=models.SlugField(default=b'slug_placeholder', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='slug',
            field=models.SlugField(default=b'slug_placeholder', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 8, 22, 4, 46, 38257, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='resources',
            field=models.ManyToManyField(related_name='projects', to='taskmaster_app.Resource', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 8, 22, 4, 46, 40832, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='resources',
            field=models.ManyToManyField(related_name='tasks', to='taskmaster_app.Resource', blank=True),
            preserve_default=True,
        ),
    ]
