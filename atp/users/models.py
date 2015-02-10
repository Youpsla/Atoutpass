# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.db import models
from django.contrib.auth.models import AbstractUser


# Subclass AbstractUser
class User(AbstractUser):
    TYPES = (('CL', 'Client'),
             ('AG', 'Agent'))
    type = models.CharField(max_length=2, blank=True, default='CL', choices=TYPES)

    def __unicode__(self):
        return 'User: %s' % self.username
