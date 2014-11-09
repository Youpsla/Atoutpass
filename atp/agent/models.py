# -*- coding: utf-8 -*-
from django.db import models
from config.common import Common
from django.utils.translation import ugettext_lazy as _
import datetime
from jsonfield import JSONField
from collections import OrderedDict


class Certification(models.Model):
    short_name = models.CharField('Nom court', max_length=24, blank=False)
    long_name = models.CharField('Nom long', max_length=240, blank=False)

    def __unicode__(self):
        return self.long_name


class Qualification(models.Model):
    short_name = models.CharField('Nom court', max_length=24, blank=False)
    long_name = models.CharField('Nom long', max_length=240, blank=False)

    def __unicode__(self):
        return self.long_name


AGENT_FORM_STATE = OrderedDict([
    ('NOM_PRENOM', 0),
    ('AGENT', 0),
    ('COORDONNEES', 0),
    ('PAPIERS_IDENTITE', 0),
    ('CARTE_PRO', 0),
    ('QUALIFICATIONS', 0),
    ('CERTIFICATIONS', 0),
    ('DIVERS', 0)
    ])


AGENT_GENRE_CHOICES = (
    ('M', 'Homme'),
    ('F', 'Femme')
)


class Agent(models.Model):
    user = models.OneToOneField(Common.AUTH_USER_MODEL, related_name='agent')
    firstname = models.CharField(_('Nom'), max_length=256, blank=True, null=True)
    lastname = models.CharField(_(u'Prénom'), max_length=256, blank=True, null=True)
    genre = models.CharField(_(u'Genre'), max_length=1, choices=AGENT_GENRE_CHOICES,
                             blank=True, null=True)
    birthdate = models.DateField(_(u'Date de naisance'), blank=True, null=True)
    birthplace = models.CharField(
        _(u'Lieu de naissance'), max_length=120, blank=True, null=True)
    nationality = models.CharField(
        _(u'Nationalité'), max_length=120, blank=True, null=True)
    vital_card_validity_start_date = models.DateTimeField(blank=True, null=True)
    vital_card_validity_end_date = models.DateTimeField(blank=True, null=True)
    vital_card_number = models.CharField(_(u'Numéro de carte vitale'), max_length='20', blank=True, null=True)
    pole_emploi_start_date = models.DateTimeField(blank=True, null=True)
    pole_emploi_end_date = models.DateTimeField(blank=True, null=True)
    certifications = models.ManyToManyField(Certification, blank=True,
                                            null=True,
                                            through='AgentCertification',
                                            related_name='agentcertifications')
    qualifications = models.ManyToManyField(Qualification, blank=True,
                                            null=True,
                                            through='AgentQualification',
                                            related_name='agentqualifications')
    is_completed = models.BooleanField(_('Profil complet'), default=False,)
    picture = models.ImageField(_(u'Photo identité'),
                                blank=True, null=True)
    last_modified = models.DateTimeField(auto_now_add=True, blank=True)
    form_state = JSONField(load_kwargs={'object_pairs_hook': OrderedDict},
                           default=AGENT_FORM_STATE)

    def __unicode__(self):
        return '%s %s' % ((self.firstname), str(self.lastname))

    def save(self, *args, **kwargs):
        self.last_modified = datetime.datetime.today()
        return super(Agent, self).save(*args, **kwargs)


class AgentCertification(models.Model):
    agent = models.ForeignKey(Agent, related_name="agent_certifications")
    certification = models.ForeignKey(Certification, blank=True, null=True,
                                      default=None)
    start_date = models.DateField(_(u'Date de début'), blank=True, null=True)
    end_date = models.DateField(_(u'Date de fin'), blank=True, null=True)
    picture = models.ImageField("Document officiel", blank=True, null=True)

    def __unicode__(self):
        return unicode(self.certification)


class AgentQualification(models.Model):
    agent = models.ForeignKey(Agent, related_name="agent_qualifications")
    qualification = models.ForeignKey(Qualification, blank=True, null=True,
                                      default=None)
    start_date = models.DateField(_(u'Date de début'), blank=True, null=True)
    end_date = models.DateField(_(u'Date de fin'), blank=True, null=True)

    def __unicode__(self):
        return unicode(self.qualification)


PROCARD_CHOICES = ((True, 'Titulaire'), (False, 'Pas titulaire'))


class AgentProCard(models.Model):
    agent = models.ForeignKey(Agent)
    pro_card = models.BooleanField(
        _(u'Etes-vous titulaire de la carte professionnelle ?'),
        choices=PROCARD_CHOICES,
        blank=True, default=False)
    pro_card_validity_start_date = models.DateField(
        _(u'Date de début de validité'), blank=True, null=True)
    pro_card_validity_end_date = models.DateField(
        _(u'Date de fin de validité'), blank=True, null=True)
    pro_card_front = models.ImageField(
        _(u'Recto de votre carte professionnelle'), blank=True, null=True,
        upload_to='.')
    pro_card_number = models.CharField(_(u'Numéro'), max_length='15', blank=True, null=True)
    last_modified = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return unicode(self.pro_card)

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
    id_card_validity_start_date = models.DateField(
        _(u'Date de début de validité'), blank=True, null=True)
    id_card_validity_end_date = models.DateField(
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
    agent = models.ForeignKey(Agent, related_name='agent_address')
    address1 = models.CharField(_('Adresse 1'), max_length=120, blank=True)
    address2 = models.CharField(_('Adresse 2'), max_length=120, blank=True)
    zipcode = models.CharField(_('Code Postal'), max_length=5, blank=True)
    city = models.CharField(_('Ville'), max_length=120, blank=True)
    mobilephonenumber = models.CharField(
        _(u'Téléphone mobile'), max_length=10, blank=True, null=True)
    fixephonenumber = models.CharField(
        _(u'Téléphone fixe'), max_length=10, blank=True, null=True)

    last_modified = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.address1

    def save(self, *args, **kwargs):
        self.last_modified = datetime.datetime.today()
        return super(AgentAddress, self).save(*args, **kwargs)


CAR_LICENSE_TYPE = (
    ('B', 'Permis B'),
    ('C', 'Permis C'),
    ('D', 'Permis D'),
    ('E', 'Permis E'),
)

CAR_CHOICES = ((True, 'Oui'), (False, 'Non'))

class AgentVarious(models.Model):
    agent = models.ForeignKey(Agent)
    english = models.BooleanField(choices=CAR_CHOICES, blank=True, default=False)
    german = models.BooleanField(choices=CAR_CHOICES, blank=True, default=False)
    spanish = models.BooleanField(choices=CAR_CHOICES, blank=True, default=False)
    has_car = models.BooleanField(choices=CAR_CHOICES, blank=True, default=False)
    has_motorbike = models.BooleanField(choices=CAR_CHOICES, blank=True, default=False)
    has_car_license = models.BooleanField(choices=CAR_CHOICES, blank=True, default=False)
    has_motorbike_license = models.BooleanField(choices=CAR_CHOICES, blank=True, default=False)
    car_license_type = models.CharField(max_length=1, choices=CAR_LICENSE_TYPE,
                                        blank=True, null=True)
    car_license_start_date = models.DateField(
        blank=True, null=True)
    car_license_end_date = models.DateField(
        blank=True, null=True)

    last_modified = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.car_license_type

    def save(self, *args, **kwargs):
        self.last_modified = datetime.datetime.today()
        return super(AgentVarious, self).save(*args, **kwargs)


class Countries(models.Model):
    alpha2 = models.CharField('Code 2 lettre', max_length=2)
    alpha3 = models.CharField('Code 3 lettres', max_length=3)
    name = models.CharField('Nom Pays', max_length=128)
