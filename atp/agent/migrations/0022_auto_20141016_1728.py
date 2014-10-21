# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0021_agent_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address1', models.CharField(max_length=120, verbose_name='Adresse 1', blank=True)),
                ('address2', models.CharField(max_length=120, verbose_name='Adresse 2', blank=True)),
                ('zipcode', models.CharField(max_length=5, verbose_name='Code Postal', blank=True)),
                ('city', models.CharField(max_length=120, verbose_name='Ville', blank=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(to='agent.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentIdCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_card_type', models.CharField(max_length=120, null=True, verbose_name='Type de papier', blank=True)),
                ('id_card_validity_start_date', models.DateTimeField(null=True, blank=True)),
                ('id_card_validity_end_date', models.DateTimeField(null=True, blank=True)),
                ('id_card_front', models.ImageField(null=True, upload_to=b'.', blank=True)),
                ('id_card_back', models.ImageField(null=True, upload_to=b'.', blank=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(to='agent.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='agent',
            name='address1',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='city',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='id_card_type',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='id_card_validity_end_date',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='id_card_validity_start_date',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='zipcode',
        ),
        migrations.AlterField(
            model_name='agent',
            name='picture',
            field=models.ImageField(upload_to=b'', null=True, verbose_name=b'Document officiel', blank=True),
        ),
    ]
