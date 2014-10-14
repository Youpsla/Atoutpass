# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0002_agent_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='poleemploi',
            name='end_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poleemploi',
            name='start_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='address2',
            field=models.CharField(max_length=120, null=True, verbose_name=b'Adresse 2', blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='birthdate',
            field=models.DateField(default=b'2000-01-01'),
        ),
        migrations.AlterField(
            model_name='poleemploi',
            name='pole_emploi',
            field=models.BooleanField(default=False, verbose_name=b'Pole_ Emploi'),
        ),
    ]
