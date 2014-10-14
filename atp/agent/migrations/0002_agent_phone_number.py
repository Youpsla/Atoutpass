# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='phone_number',
            field=models.CharField(default='0123456789', max_length=15, verbose_name=b'Telephone'),
            preserve_default=False,
        ),
    ]
