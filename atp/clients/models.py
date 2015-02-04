# -*- coding: utf-8 -*-
from django.db import models
from config.common import Common
from django.utils.translation import ugettext_lazy as _
from agent.models import Agent
from django_fsm import FSMKeyField, transition
import datetime
from django.db.models.signals import post_save


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


from django.middleware import csrf
def get_or_create_csrf_token(request):
    token = request.META.get('CSRF_COOKIE', None)
    if token is None:
        token = csrf._get_new_csrf_key()
        request.META['CSRF_COOKIE'] = token
    request.META['CSRF_COOKIE_USED'] = True
    return token


class SelectionQuerySet(models.QuerySet):
    def for_user(self, user):
        print "UUSSEERR :", user
        return self.filter(client=user)


class Selection(models.Model):
    client = models.ForeignKey(Client, related_name='client')
    start_date = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now_add=True, blank=True)
    state = FSMKeyField(States, default='new', protected=True, blank=True, null=True, related_name='selection_state')
    name = models.CharField(_('Nom'), max_length=120, blank=True, null=True)
    description = models.CharField(_('Description'), max_length=220, blank=True, null=True)
    agents = models.ManyToManyField(Agent, blank=True,
                                            null=True,
                                            through='SelectionAgentsRelationship',
                                            related_name='agents')

    def save(self, *args, **kwargs):
        self.last_modified = datetime.datetime.today()
        return super(Selection, self).save(*args, **kwargs)
    
    @transition(field=state, source='new', target='validated')
    def validate(self):
        print "Selection state update to created"
        pass

    @transition(field=state, source='validated', target='payed')
    def payed(self):
        pass
    
    @transition(field=state, source='payed', target='pdf_generated')
    def generate_pdf(self):
        pass
    
    @transition(field=state, source='pdf_generated', target='exported')
    def export(self):
        pass
    
    def add_action_button(self, **kwargs):
        if self.state == 'created':
            return """<a class='btn' href="/client/~client/data?selectionid=%s">""" % (self.id)
        else:
            return """bloque"""

    objects = SelectionQuerySet.as_manager()

post_save.connect(Selection().validate, Selection, dispatch_uid="Selection_validated")

class SelectionAgentsRelationship(models.Model):
    agent = models.ForeignKey(Agent, blank=True, null=True)
    selection = models.ForeignKey(Selection, blank=True, null=True)
   
    def __unicode__(self):
        return unicode(self.selection)

    class Meta():
        auto_created=True
