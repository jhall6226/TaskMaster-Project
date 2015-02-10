# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taskmaster_app', '0005_auto_20150208_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 8, 23, 57, 47, 32809, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='resources',
            field=models.ManyToManyField(related_name='projects', to='taskmaster_app.Resource'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 8, 23, 57, 47, 35530, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='resources',
            field=models.ManyToManyField(related_name='tasks', to='taskmaster_app.Resource'),
            preserve_default=True,
        ),
    ]
