# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0010_auto_20141005_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='certifications',
            field=models.ManyToManyField(to='agent.Certification', null=True, through='agent.AgentCertification', blank=True),
            preserve_default=True,
        ),
    ]
