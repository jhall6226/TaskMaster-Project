# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taskmaster_app', '0009_auto_20150210_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='attachments',
            field=models.FileField(upload_to=b'projects/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 11, 1, 41, 15, 697735, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 11, 1, 41, 15, 700275, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
