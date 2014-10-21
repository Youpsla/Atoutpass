# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import agent.models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0014_auto_20141015_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='picture',
            field=models.ImageField(null=True, verbose_name=b'Document officiel', blank=True),
            preserve_default=True,
        ),
    ]
