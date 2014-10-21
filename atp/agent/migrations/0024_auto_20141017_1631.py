# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0023_auto_20141017_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentcertification',
            name='certification',
            field=models.ForeignKey(blank=True, to='agent.Certification', null=True),
        ),
    ]
