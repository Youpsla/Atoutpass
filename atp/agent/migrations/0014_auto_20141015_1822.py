# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import agent.models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0013_auto_20141010_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentcertification',
            name='picture',
            field=models.ImageField(null=True, verbose_name=b'Document officiel', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(related_name=b'agent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='agentcertification',
            name='agent',
            field=models.ForeignKey(related_name=b'agent_certifications', to='agent.Agent'),
        ),
    ]
