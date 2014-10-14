# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agent', '0003_auto_20141005_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Certification',
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
            model_name='agentcertification',
            name='certification',
            field=models.ForeignKey(to='agent.Certification'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agentcertification',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
