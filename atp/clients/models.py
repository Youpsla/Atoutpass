# -*- coding: utf-8 -*-
from django.db import models
from config.common import Common
from django.utils.translation import ugettext_lazy as _

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
