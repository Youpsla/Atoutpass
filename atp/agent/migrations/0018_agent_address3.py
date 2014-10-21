# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0017_auto_20141015_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='address3',
            field=models.CharField(default='sasa', max_length=120, verbose_name='Adresse 1', blank=True),
            preserve_default=False,
        ),
    ]
