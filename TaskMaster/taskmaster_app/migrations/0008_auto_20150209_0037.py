# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taskmaster_app', '0007_auto_20150209_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 9, 0, 37, 5, 406998, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 9, 0, 37, 5, 409466, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
