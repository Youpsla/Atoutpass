# -*- coding: utf-8 -*-
from django.db import models
from config.common import Common
from django.utils.translation import ugettext_lazy as _
import datetime
from jsonfield import JSONField


class Certification(models.Model):
    short_name = models.CharField('Nom court', max_length=24, blank=False)
    long_name = models.CharField('Nom long', max_length=240, blank=False)

    def __unicode__(self):
        return self.long_name


# Init of Agent state form.
AGENT_FORM_STATE = {
    'AGENT': 0,
    # 'NOM_PRENOM': 0,
    'COORDONNEES': 0,
    'PAPIERS_IDENTITE': 0,
    'CARTE_PRO': 0,
    'CERTIFICATIONS': 0
}


AGENT_GENRE_CHOICES = (
    ('M', 'Homme'),
    ('F', 'Femme')
)


class Agent(models.Model):
    user = models.OneToOneField(Common.AUTH_USER_MODEL, related_name='agent')
    genre = models.CharField(max_length=1, choices=AGENT_GENRE_CHOICES,
                             blank=True, null=True)
    birthdate = models.DateField('Date de naisance', blank=True, null=True)
    birthplace = models.CharField(
        _('Lieu de naissance'), max_length=120, blank=True, null=True)
    nationality = models.CharField(
        _('Nationalite'), max_length=120, blank=True, null=True)
    vital_card_validity_start_date = models.DateTimeField(blank=True, null=True)
    vital_card_validity_end_date = models.DateTimeField(blank=True, null=True)
    pole_emploi_start_date = models.DateTimeField(blank=True, null=True)
    pole_emploi_end_date = models.DateTimeField(blank=True, null=True)
    driver_license_type = models.CharField(max_length=120, blank=True,
                                           null=True)
    certifications = models.ManyToManyField(Certification, blank=True,
                                            null=True,
                                            through='AgentCertification',)
    is_completed = models.BooleanField(_('Profil complet'), default=False,)
    picture = models.ImageField("Document officiel",
                                blank=True, null=True)
    last_modified = models.DateTimeField(auto_now_add=True, blank=True)
    form_state = JSONField(default=AGENT_FORM_STATE)

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.last_modified = datetime.datetime.today()
        return super(Agent, self).save(*args, **kwargs)


PROCARD_CHOICES = ((True, 'Titulaire'), (False, 'Pas titulaire'))


class AgentProCard(models.Model):
    agent = models.ForeignKey(Agent)
    pro_card = models.BooleanField(
        _(u'Etes-vous titulaire de la carte professionnelle ?'),
        choices=PROCARD_CHOICES,
        blank=True, default=False)
    pro_card_validity_start_date = models.DateTimeField(
        _(u'Date de début de validité'), blank=True, null=True)
    pro_card_validity_end_date = models.DateTimeField(
        _(u'Date de fin de validité'), blank=True, null=True)
    pro_card_front = models.ImageField(
        _(u'Recto de votre carte professionnelle'), blank=True, null=True,
        upload_to='.')

    last_modified = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return unicode(self.id_card_type)

    def save(self, *args, **kwargs):
        self.last_modified = datetime.datetime.today()
        return super(AgentProCard, self).save(*args, **kwargs)


class AgentIdCard(models.Model):

    ID_CARD_TYPES = (
        ('CNI', 'Carte identite'),
        ('PP', 'Passeport'),
        ('CJ', 'Carte de sejour'),
    )

    agent = models.ForeignKey(Agent)
    id_card_type = models.CharField(
        _('Type de papier'), max_length=120, choices=ID_CARD_TYPES, default=1,
        blank=True, null=True)
    id_card_validity_start_date = models.DateTimeField(
        _(u'Date de début de validité'), blank=True, null=True)
    id_card_validity_end_date = models.DateTimeField(
        _(u'Date de fin de validité'), blank=True, null=True)
    id_card_front = models.ImageField(
        _(u'Recto de votre pièce'), blank=True, null=True, upload_to='.')
    id_card_back = models.ImageField(
        _(u'Verso de votre pièce'), blank=True, null=True, upload_to='.')

    last_modified = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return unicode(self.id_card_type)

    def save(self, *args, **kwargs):
        self.last_modified = datetime.datetime.today()
        return super(AgentIdCard, self).save(*args, **kwargs)


class AgentAddress(models.Model):
    agent = models.ForeignKey(Agent)
    address1 = models.CharField(_('Adresse 1'), max_length=120, blank=True)
    address2 = models.CharField(_('Adresse 2'), max_length=120, blank=True)
    zipcode = models.CharField(_('Code Postal'), max_length=5, blank=True)
    city = models.CharField(_('Ville'), max_length=120, blank=True)
    mobilephonenumber = models.IntegerField(
        _('Mobile'), max_length=10, blank=True, null=True)
    fixephonenumber = models.IntegerField(
        _('Fixe'), max_length=10, blank=True, null=True)

    last_modified = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.address1

    def save(self, *args, **kwargs):
        self.last_modified = datetime.datetime.today()
        return super(AgentAddress, self).save(*args, **kwargs)


class PoleEmploi(models.Model):
    agent = models.ForeignKey(Agent)
    pole_emploi = models.BooleanField('Pole_ Emploi', default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.pole_emploi


class AgentCertification(models.Model):
    agent = models.ForeignKey(Agent, related_name="agent_certifications")
    certification = models.ForeignKey(Certification, blank=True, null=True,
                                      default=None)
    start_date = models.DateField(_(u'Date de début'), blank=True, null=True)
    end_date = models.DateField(_(u'Date de fin'), blank=True, null=True)
    picture = models.ImageField("Document officiel", blank=True, null=True)

    def __unicode__(self):
        return self.certification


class Countries(models.Model):
    alpha2 = models.CharField('Code 2 lettre', max_length=2)
    alpha3 = models.CharField('Code 3 lettres', max_length=3)
    name = models.CharField('Nom Pays', max_length=128)
