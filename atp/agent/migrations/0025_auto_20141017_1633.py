# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0024_auto_20141017_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentcertification',
            name='end_date',
            field=models.DateField(null=True, verbose_name='Date de fin', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agentcertification',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Date de d\xe9but', blank=True),
        ),
    ]
