# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django_fsm
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
                ('firstname', models.CharField(max_length=256, null=True, verbose_name='Nom', blank=True)),
                ('lastname', models.CharField(max_length=256, null=True, verbose_name='Pr\xe9nom', blank=True)),
                ('genre', models.CharField(blank=True, max_length=1, null=True, verbose_name='Genre', choices=[(b'M', b'Homme'), (b'F', b'Femme')])),
                ('birthdate', models.DateField(null=True, verbose_name='Date de naisance', blank=True)),
                ('birthplace', models.CharField(max_length=120, null=True, verbose_name='Lieu de naissance', blank=True)),
                ('nationality', models.CharField(max_length=120, null=True, verbose_name='Nationalit\xe9', blank=True)),
                ('vital_card_validity_start_date', models.DateTimeField(null=True, blank=True)),
                ('vital_card_validity_end_date', models.DateTimeField(null=True, blank=True)),
                ('vital_card_number', models.CharField(max_length=b'20', null=True, verbose_name='Num\xe9ro de carte vitale', blank=True)),
                ('pole_emploi_start_date', models.DateTimeField(null=True, blank=True)),
                ('pole_emploi_end_date', models.DateTimeField(null=True, blank=True)),
                ('is_completed', models.BooleanField(default=False, verbose_name='Profil complet')),
                ('picture', models.ImageField(upload_to=b'', null=True, verbose_name='Photo identit\xe9', blank=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('form_state', jsonfield.fields.JSONField(default={b'NOM_PRENOM': 0, b'AGENT': 0, b'COORDONNEES': 0, b'PAPIERS_IDENTITE': 0, b'CARTE_PRO': 0, b'QUALIFICATIONS': 0, b'CERTIFICATIONS': 0, b'DIVERS': 0})),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address1', models.CharField(max_length=120, verbose_name='Adresse 1', blank=True)),
                ('address2', models.CharField(max_length=120, verbose_name='Adresse 2', blank=True)),
                ('zipcode', models.CharField(max_length=5, verbose_name='Code Postal', blank=True)),
                ('city', models.CharField(max_length=120, verbose_name='Ville', blank=True)),
                ('mobilephonenumber', models.CharField(max_length=10, null=True, verbose_name='T\xe9l\xe9phone mobile', blank=True)),
                ('fixephonenumber', models.CharField(max_length=10, null=True, verbose_name='T\xe9l\xe9phone fixe', blank=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(to='agent.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='Date de d\xe9but', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='Date de fin', blank=True)),
                ('picture', models.ImageField(upload_to=b'', null=True, verbose_name=b'Document officiel', blank=True)),
                ('agent', models.ForeignKey(related_name='agent_certifications', to='agent.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentIdCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_card_type', models.CharField(default=1, choices=[(b'CNI', b'Carte identite'), (b'PP', b'Passeport'), (b'CJ', b'Carte de sejour')], max_length=120, blank=True, null=True, verbose_name='Type de papier')),
                ('id_card_validity_start_date', models.DateField(null=True, verbose_name='Date de d\xe9but de validit\xe9', blank=True)),
                ('id_card_validity_end_date', models.DateField(null=True, verbose_name='Date de fin de validit\xe9', blank=True)),
                ('id_card_front', models.ImageField(upload_to=b'.', null=True, verbose_name='Recto de votre pi\xe8ce', blank=True)),
                ('id_card_back', models.ImageField(upload_to=b'.', null=True, verbose_name='Verso de votre pi\xe8ce', blank=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(related_name='idcard', to='agent.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentProCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pro_card', models.BooleanField(default=False, verbose_name='Etes-vous titulaire de la carte professionnelle ?', choices=[(True, b'Titulaire'), (False, b'Pas titulaire')])),
                ('pro_card_validity_start_date', models.DateField(null=True, verbose_name='Date de d\xe9but de validit\xe9', blank=True)),
                ('pro_card_validity_end_date', models.DateField(null=True, verbose_name='Date de fin de validit\xe9', blank=True)),
                ('pro_card_front', models.ImageField(upload_to=b'.', null=True, verbose_name='Recto de votre carte professionnelle', blank=True)),
                ('pro_card_number', models.CharField(max_length=b'15', null=True, verbose_name='Num\xe9ro', blank=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(related_name='procard', to='agent.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='Date de d\xe9but', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='Date de fin', blank=True)),
                ('agent', models.ForeignKey(related_name='agent_qualifications', to='agent.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentVarious',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english', models.BooleanField(default=False, choices=[(True, b'Oui'), (False, b'Non')])),
                ('german', models.BooleanField(default=False, choices=[(True, b'Oui'), (False, b'Non')])),
                ('spanish', models.BooleanField(default=False, choices=[(True, b'Oui'), (False, b'Non')])),
                ('has_car', models.BooleanField(default=False, choices=[(True, b'Oui'), (False, b'Non')])),
                ('has_motorbike', models.BooleanField(default=False, choices=[(True, b'Oui'), (False, b'Non')])),
                ('has_car_license', models.BooleanField(default=False, choices=[(True, b'Oui'), (False, b'Non')])),
                ('has_motorbike_license', models.BooleanField(default=False, choices=[(True, b'Oui'), (False, b'Non')])),
                ('car_license_type', models.CharField(blank=True, max_length=1, null=True, choices=[(b'B', b'Permis B'), (b'C', b'Permis C'), (b'D', b'Permis D'), (b'E', b'Permis E')])),
                ('car_license_start_date', models.DateField(null=True, blank=True)),
                ('car_license_end_date', models.DateField(null=True, blank=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(to='agent.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AreaDepartment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=128)),
                ('name_cap', models.CharField(max_length=128)),
                ('name_url', models.CharField(max_length=128)),
                ('soundex', models.CharField(max_length=16)),
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
                'verbose_name': 'dede verbose_name',
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=24, verbose_name=b'Nom court')),
                ('long_name', models.CharField(max_length=240, verbose_name=b'Nom long')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='agentqualification',
            name='qualification',
            field=models.ForeignKey(default=None, blank=True, to='agent.Qualification', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agentcertification',
            name='certification',
            field=models.ForeignKey(default=None, blank=True, to='agent.Certification', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agentaddress',
            name='area_department',
            field=models.ForeignKey(to='agent.AreaDepartment', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='certifications',
            field=models.ManyToManyField(related_name='agentcertifications', null=True, through='agent.AgentCertification', to='agent.Certification', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='qualifications',
            field=models.ManyToManyField(related_name='agentqualifications', null=True, through='agent.AgentQualification', to='agent.Qualification', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='state',
            field=django_fsm.FSMKeyField(default=b'new', to='agent.States', protected=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(related_name='users_agent', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
