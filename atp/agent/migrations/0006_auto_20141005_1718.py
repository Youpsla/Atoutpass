# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agent', '0005_auto_20141005_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('certification', models.ForeignKey(to='agent.Certification')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='agentcertification',
            name='certification',
        ),
        migrations.RemoveField(
            model_name='agentcertification',
            name='user',
        ),
        migrations.DeleteModel(
            name='AgentCertification',
        ),
    ]
