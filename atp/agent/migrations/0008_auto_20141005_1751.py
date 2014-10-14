# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0007_auto_20141005_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('agent', models.ForeignKey(to='agent.Agent')),
                ('certification', models.ForeignKey(to='agent.Certification')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='usercertification',
            name='agent',
        ),
        migrations.RemoveField(
            model_name='usercertification',
            name='certification',
        ),
        migrations.DeleteModel(
            name='UserCertification',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='agent',
            name='birthplace',
            field=models.CharField(max_length=120, null=True, verbose_name='Lieu de naissance', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='driver_license_type',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='id_card_type',
            field=models.CharField(max_length=120, null=True, verbose_name='Type de papier', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='id_card_validity_end_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='id_card_validity_start_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Profil complet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='nationality',
            field=models.CharField(max_length=120, null=True, verbose_name='Nationalite', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='phonenumber',
            field=models.IntegerField(max_length=10, null=True, verbose_name='Telephone', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='pole_emploi_end_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='pole_emploi_start_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='pro_card',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agent',
            name='pro_card_validity_end_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='pro_card_validity_start_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='vital_card_validity_end_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='vital_card_validity_start_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='address1',
            field=models.CharField(max_length=120, verbose_name='Adresse 1', blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='address2',
            field=models.CharField(max_length=120, verbose_name='Adresse 2', blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='birthdate',
            field=models.DateField(default=b'2000-01-01', blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='city',
            field=models.CharField(max_length=120, verbose_name='Ville', blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='zipcode',
            field=models.CharField(max_length=5, verbose_name='Code Postal', blank=True),
        ),
        migrations.AlterField(
            model_name='poleemploi',
            name='agent',
            field=models.ForeignKey(to='agent.Agent'),
        ),
    ]
