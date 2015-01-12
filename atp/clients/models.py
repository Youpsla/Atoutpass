# -*- coding: utf-8 -*-
from django.db import models
from config.common import Common
from django.utils.translation import ugettext_lazy as _
from agent.models import Agent
from django_fsm import FSMKeyField, transition
import datetime


# Create your models here.

CLIENT_GENRE_CHOICES = (
    ('M', 'Homme'),
    ('F', 'Femme')
)


class Client(models.Model):
    user = models.OneToOneField(Common.AUTH_USER_MODEL, related_name='users_client')
    firstname = models.CharField(_(u'Nom'), max_length=256, blank=True, null=True)
    lastname = models.CharField(_(u'Prénom'), max_length=256, blank=True, null=True)
    genre = models.CharField(_(u'Genre'), max_length=1, choices=CLIENT_GENRE_CHOICES,
                             blank=True, null=True)
    company = models.CharField(_(u'Entreprise'), max_length=256, blank=True, null=True)
    mobilephonenumber = models.CharField(
        _(u'Téléphone mobile'), max_length=10, blank=True, null=True)
    phonenumber = models.CharField(
        _(u'Téléphone fixe'), max_length=10, blank=True, null=True)
    address1 = models.CharField(_('Adresse 1'), max_length=120, blank=True)
    address2 = models.CharField(_('Adresse 2'), max_length=120, blank=True)
    zipcode = models.CharField(_('Code Postal'), max_length=5, blank=True)
    city = models.CharField(_('Ville'), max_length=120, blank=True)

    def __unicode__(self):
        return '%s %s - %s' % (self.firstname, self.lastname, self.company)


class States(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    label = models.CharField(max_length=255)

    def __unicode__(self):
        return self.label


class Selection(models.Model):
    client = models.ForeignKey(Client, related_name='selection_client')
    start_date = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now_add=True, blank=True)
    state = FSMKeyField(States, default='new', protected=True, blank=True, null=True)
    name = models.CharField(_('Nom'), max_length=120, blank=True, null=True)
    description = models.CharField(_('Description'), max_length=220, blank=True, null=True)
    agents = models.ManyToManyField(Agent, blank=True,
                                            null=True,
                                            through='SelectionAgentsRelationship',
                                            related_name='selectionagents')


    def save(self, *args, **kwargs):
        self.last_modified = datetime.datetime.today()
        return super(Selection, self).save(*args, **kwargs)

    @transition(field=state, source='new', target='created')
    def create(self):
        pass

    @transition(field=state, source='created', target='pending')
    def fill(self):
        pass


class SelectionAgentsRelationship(models.Model):
    agent = models.ForeignKey(Agent, related_name="selection_agents")
    selection = models.ForeignKey(Selection, blank=True, null=True,
                                      default=None)
   
    def __unicode__(self):
        return unicode(self.selection)

    class Meta():
        auto_created=True
