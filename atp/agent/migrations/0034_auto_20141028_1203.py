# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0033_auto_20141023_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poleemploi',
            name='agent',
        ),
        migrations.DeleteModel(
            name='PoleEmploi',
        ),
        migrations.AlterField(
            model_name='agent',
            name='form_state',
            field=jsonfield.fields.JSONField(default={b'NOM_PRENOM': 0, b'AGENT': 0, b'COORDONNEES': 0, b'PAPIERS_IDENTITE': 0, b'CARTE_PRO': 0, b'CERTIFICATIONS': 0}),
        ),
    ]
