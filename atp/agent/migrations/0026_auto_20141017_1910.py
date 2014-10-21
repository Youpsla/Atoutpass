# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0025_auto_20141017_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentProCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pro_card', models.BooleanField(default=0, verbose_name='Etes-vous titulaire de la carte professionnelle')),
                ('pro_card_validity_start_date', models.DateTimeField(null=True, verbose_name='Date de d\xe9but de validit\xe9', blank=True)),
                ('pro_card_validity_end_date', models.DateTimeField(null=True, verbose_name='Date de fin de validit\xe9', blank=True)),
                ('pro_card_front', models.ImageField(upload_to=b'.', null=True, verbose_name='Recto de votre carte professionnelle', blank=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(to='agent.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='agent',
            name='pro_card',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='pro_card_validity_end_date',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='pro_card_validity_start_date',
        ),
        migrations.AlterField(
            model_name='agentcertification',
            name='certification',
            field=models.ForeignKey(default=None, blank=True, to='agent.Certification', null=True),
        ),
    ]
