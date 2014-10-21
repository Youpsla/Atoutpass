# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0015_agent_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now, auto_now_add=True),
            preserve_default=False,
        ),
    ]
