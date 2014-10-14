from django.db import models
from config.common import Common
from django.utils.translation import ugettext_lazy as _


#class Agent(models.Model):
    #user = models.OneToOneField(Common.AUTH_USER_MODEL)
    #birthdate = models.DateField(default='2000-01-01')
    #address1 = models.CharField('Adresse 1', max_length=120)
    #address2 = models.CharField('Adresse 2', max_length=120, blank=True, null=True)
    #zipcode = models.CharField('Code Postal', max_length=5)
    #city = models.CharField('Ville', max_length=120)
    #phone_number = models.CharField('Telephone', max_length=15)

    #def __unicode__(self):
        #return self.user.username


#class PoleEmploi(models.Model):
    #user = models.OneToOneField(Common.AUTH_USER_MODEL)
    #pole_emploi = models.BooleanField('Pole_ Emploi', default=False)
    #start_date = models.DateField(blank=True, null=True)
    #end_date = models.DateField(blank=True, null=True)

    #def __unicode__(self):
        #return self.pole_emploi


#class Certification(models.Model):
    #short_name = models.CharField('Nom court', max_length=24, blank=False)
    #long_name = models.CharField('Nom long', max_length=240, blank=False)

    #def __unicode__(self):
        #return self.long_name


#class UserCertification(models.Model):
    #user = models.ForeignKey(Common.AUTH_USER_MODEL)
    #certification = models.ForeignKey(Certification)
    #start_date = models.DateField(blank=False, null=False)
    #end_date = models.DateField(blank=False, null=False)

    #def __unicode__(self):
        #return self.certification

class Certification(models.Model):
    short_name = models.CharField('Nom court', max_length=24, blank=False)
    long_name = models.CharField('Nom long', max_length=240, blank=False)

    def __unicode__(self):
        return self.long_name




class Agent(models.Model):
    user = models.OneToOneField(Common.AUTH_USER_MODEL, related_name='agent')
    birthdate = models.DateField('Date de naisance', blank=True, null=True)
    address1 = models.CharField(_('Adresse 1'), max_length=120, blank=True)
    address2 = models.CharField(_('Adresse 2'), max_length=120, blank=True)
    zipcode = models.CharField(_('Code Postal'), max_length=5, blank=True)
    city = models.CharField(_('Ville'), max_length=120, blank=True)
    phonenumber = models.IntegerField(
        _('Telephone'), max_length=10, blank=True, null=True)
    birthplace = models.CharField(
        _('Lieu de naissance'), max_length=120, blank=True, null=True)
    nationality = models.CharField(
        _('Nationalite'), max_length=120, blank=True, null=True)
    id_card_type = models.CharField(
        _('Type de papier'), max_length=120, blank=True, null=True)
    id_card_validity_start_date = models.DateTimeField(blank=True, null=True)
    id_card_validity_end_date = models.DateTimeField(blank=True, null=True)
    vital_card_validity_start_date = models.DateTimeField(blank=True, null=True)
    vital_card_validity_end_date = models.DateTimeField(blank=True, null=True)
    # id_card_front = models.ImageField(blank=True, null=True, upload_to='.')
    # id_card_back = models.ImageField(blank=True, null=True, upload_to='.')
    pole_emploi_start_date = models.DateTimeField(blank=True, null=True)
    pole_emploi_end_date = models.DateTimeField(blank=True, null=True)
    driver_license_type = models.CharField(max_length=120, blank=True, null=True)
    pro_card = models.BooleanField('Carte professionnelle', blank=True, default=0)
    pro_card_validity_start_date = models.DateTimeField('Date de debut de validite', blank=True, null=True)
    pro_card_validity_end_date = models.DateTimeField('Date de fin de validite', blank=True, null=True)
    certifications = models.ManyToManyField(Certification, blank=True, null=True, through='AgentCertification',)
    is_completed = models.BooleanField(_('Profil complet'), default=False,)

    def __unicode__(self):
        return self.user.username


class PoleEmploi(models.Model):
    agent = models.ForeignKey(Agent)
    pole_emploi = models.BooleanField('Pole_ Emploi', default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.pole_emploi




class AgentCertification(models.Model):
    agent = models.ForeignKey(Agent, related_name="agent_certifications")
    certification = models.ForeignKey(Certification)
    start_date = models.DateField(blank=False, null=False)

    def __unicode__(self):
        return self.certification

