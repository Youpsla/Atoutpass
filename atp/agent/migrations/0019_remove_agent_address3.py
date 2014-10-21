# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0018_agent_address3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='address3',
        ),
    ]
