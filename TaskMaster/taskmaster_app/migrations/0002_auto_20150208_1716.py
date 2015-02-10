# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskmaster_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='email',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='name',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='position',
        ),
        migrations.AddField(
            model_name='project',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 8, 17, 16, 8, 134865, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resource',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='complexity',
            field=models.CharField(blank=True, max_length=2, choices=[(b'L', b'Low - 1'), (b'ML', b'Medium-Low - 2'), (b'M', b'Medium - 3'), (b'MH', b'Medium-High - 4'), (b'H', b'High - 5')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='estimated_time',
            field=models.FloatField(default=1.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(default=b'NS', max_length=2, choices=[(b'NS', b'Not yet started'), (b'IP', b'In progress'), (b'RR', b'Ready for review'), (b'CP', b'CP')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 8, 17, 16, 8, 137291, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
