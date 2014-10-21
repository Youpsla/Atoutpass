# -*- coding: utf-8 -*-


from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import resolve_url
from datetime import datetime, timedelta

from config.common import Common

class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):

        assert request.user.is_authenticated()
        print Common.AGENT_FORM_STATE

        try:
            agent_form = request.user.agent.agent_form
        except:
            pass
            #Agent.filter(id=id).update(field=F('field') +1))

            #pass


        #print request

        #dede = request.context

        ## context['AGENT_FORM_SATE'] =

        #if last_modified is not null:




        #if (request.user.last_login - request.user.date_joined).seconds < threshold:
            #url = '/registration/success'
        #else:
            #url = settings.LOGIN_REDIRECT_URL
        #return resolve_url(url)
        print "waoooooooooooo"
        url = settings.LOGIN_REDIRECT_URL
        return resolve_url(url)
