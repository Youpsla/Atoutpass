# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0011_agent_certifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='id_card_validity_end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='id_card_validity_start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='pole_emploi_end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='pole_emploi_start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='pro_card_validity_end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='pro_card_validity_start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='vital_card_validity_end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='vital_card_validity_start_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
