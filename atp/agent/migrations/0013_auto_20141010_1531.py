# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0012_auto_20141009_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='birthdate',
            field=models.DateField(null=True, verbose_name=b'Date de naisance', blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='pro_card',
            field=models.BooleanField(default=0, verbose_name=b'Carte professionnelle'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='pro_card_validity_end_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date de fin de validite', blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='pro_card_validity_start_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date de debut de validite', blank=True),
        ),
    ]
