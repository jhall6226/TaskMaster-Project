# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taskmaster_app', '0008_auto_20150209_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 10, 1, 7, 43, 712141, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 10, 1, 7, 43, 715600, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
