# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0008_auto_20141005_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='pro_card',
            field=models.BooleanField(default=0),
        ),
    ]
