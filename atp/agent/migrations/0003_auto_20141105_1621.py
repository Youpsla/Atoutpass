# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0002_auto_20141105_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentProCardQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='Date de d\xe9but', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='Date de fin', blank=True)),
                ('agentprocard', models.ForeignKey(related_name=b'procard_qualification', to='agent.AgentProCard')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProCardQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=24, verbose_name=b'Nom court')),
                ('long_name', models.CharField(max_length=240, verbose_name=b'Nom long')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='agentprocardqualification',
            name='procardqualification',
            field=models.ForeignKey(default=None, blank=True, to='agent.ProCardQualification', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agentprocard',
            name='qualifications',
            field=models.ManyToManyField(to='agent.ProCardQualification', null=True, through='agent.AgentProCardQualification', blank=True),
            preserve_default=True,
        ),
    ]
