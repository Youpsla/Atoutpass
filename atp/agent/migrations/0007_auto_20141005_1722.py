# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0006_auto_20141005_1718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poleemploi',
            old_name='user',
            new_name='agent',
        ),
        migrations.RemoveField(
            model_name='usercertification',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='usercertification',
            name='user',
        ),
        migrations.AddField(
            model_name='usercertification',
            name='agent',
            field=models.ForeignKey(default=1, to='agent.Agent'),
            preserve_default=False,
        ),
    ]
