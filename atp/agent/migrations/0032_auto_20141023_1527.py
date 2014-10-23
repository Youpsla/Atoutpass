# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0031_auto_20141018_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='form_state',
            field=jsonfield.fields.JSONField(default={b'PAPIERS_IDENTITE': 0, b'CARTE_PRO': 0, b'CERTIFICATIONS': 0, b'COORDONNEES': 0, b'AGENT': 0}),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='genre',
            field=models.IntegerField(blank=True, max_length=1, null=True, choices=[(b'Homme', 1), (b'Femme', 2)]),
            preserve_default=True,
        ),
    ]
