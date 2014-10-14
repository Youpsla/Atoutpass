# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0009_auto_20141005_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='birthdate',
            field=models.DateField(null=True, blank=True),
        ),
    ]
