# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0026_auto_20141017_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentprocard',
            name='pro_card',
            field=models.BooleanField(default=0, verbose_name='Etes-vous titulaire de la carte professionnelle', choices=[(True, b'Titulaire'), (False, b'pas titulaire')]),
        ),
    ]
