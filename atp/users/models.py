# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.db import models
from django.contrib.auth.models import AbstractUser


from django.utils.translation import ugettext_lazy as _


# Subclass AbstractUser
class User(AbstractUser):
    type = models.CharField(max_length = 30, blank = True, default = 'agent')

    def __unicode__(self):
        return 'User: %s' % self.username
