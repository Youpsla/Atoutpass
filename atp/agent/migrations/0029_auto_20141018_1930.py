# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0028_auto_20141017_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='phonenumber',
        ),
        migrations.AddField(
            model_name='agentaddress',
            name='fixephonenumber',
            field=models.IntegerField(max_length=10, null=True, verbose_name='Fixe', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agentaddress',
            name='mobilephonenumber',
            field=models.IntegerField(max_length=10, null=True, verbose_name='Mobile', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agentprocard',
            name='pro_card',
            field=models.BooleanField(default=False, verbose_name='Etes-vous titulaire de la carte professionnelle ?', choices=[(True, b'Titulaire'), (False, b'Pas titulaire')]),
        ),
    ]
