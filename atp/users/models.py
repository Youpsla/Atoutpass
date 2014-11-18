# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractUser


from django.utils.translation import ugettext_lazy as _


# Subclass AbstractUser
class User(AbstractUser):

    def __unicode__(self):
        #return self.username
        return self.first_name
