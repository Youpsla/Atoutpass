# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0022_auto_20141016_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentcertification',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='agentidcard',
            name='id_card_back',
            field=models.ImageField(upload_to=b'.', null=True, verbose_name='Verso de votre pi\xe8ce', blank=True),
        ),
        migrations.AlterField(
            model_name='agentidcard',
            name='id_card_front',
            field=models.ImageField(upload_to=b'.', null=True, verbose_name='Recto de votre pi\xe8ce', blank=True),
        ),
        migrations.AlterField(
            model_name='agentidcard',
            name='id_card_type',
            field=models.CharField(default=1, choices=[(b'CNI', b'Carte identite'), (b'PP', b'Passeport'), (b'CJ', b'Carte de sejour')], max_length=120, blank=True, null=True, verbose_name='Type de papier'),
        ),
        migrations.AlterField(
            model_name='agentidcard',
            name='id_card_validity_end_date',
            field=models.DateTimeField(null=True, verbose_name='Date de fin de validit\xe9', blank=True),
        ),
        migrations.AlterField(
            model_name='agentidcard',
            name='id_card_validity_start_date',
            field=models.DateTimeField(null=True, verbose_name='Date de d\xe9but de validit\xe9', blank=True),
        ),
    ]
