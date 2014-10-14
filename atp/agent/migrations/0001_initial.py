# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthdate', models.DateField()),
                ('address1', models.CharField(max_length=120, verbose_name=b'Adresse 1')),
                ('address2', models.CharField(max_length=120, verbose_name=b'Adresse 2', blank=True)),
                ('zipcode', models.CharField(max_length=5, verbose_name=b'Code Postal')),
                ('city', models.CharField(max_length=120, verbose_name=b'Ville')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PoleEmploi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pole_emploi', models.BooleanField(verbose_name=b'Pole_ Emploi')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
