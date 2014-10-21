# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0029_auto_20141018_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alpha2', models.CharField(max_length=2, verbose_name=b'Code 2 lettre')),
                ('alpha3', models.CharField(max_length=3, verbose_name=b'Code 3 lettres')),
                ('name', models.CharField(max_length=128, verbose_name=b'Nom Pays')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
