# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0020_remove_agent_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='picture',
            field=models.ImageField(upload_to=b'/images/', null=True, verbose_name=b'Document officiel', blank=True),
            preserve_default=True,
        ),
    ]
