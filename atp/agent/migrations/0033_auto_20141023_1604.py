# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0032_auto_20141023_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='genre',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', b'Homme'), (b'F', b'Femme')]),
        ),
    ]
