# -*- coding: utf8 -*-
from .models import Company
from users.models import User
from django.contrib import messages


# Create your views here.

def AddClientContextProcessor(request):
    try:
        user = request.user
        print('User trouve dans le contexte : %s' % (user))
        if user.type == 'CL':
            try:
                company = Company.objects.get(user=user.id)
                return {'client': company}
            except Company.DoesNotExist:
                messages.add_message(request, messages.WARNING, """Votre profil n'est pas complet, <b>vous ne pouvez pas créer de sélection ni passer de commande</b>. Cliquez ici pour le compléter""")
                return {'Client': None}
        else:
            return {'User_processor': 'Pas de user'}
    except User.DoesNotExist:
        #print "User non trouve"
        return {'User_processor': 'Pas de user'}
