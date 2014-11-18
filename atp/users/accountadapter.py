# -*- coding: utf-8 -*-


from allauth.account.adapter import DefaultAccountAdapter
from agent.views import agent_form_redirect
from django.core.urlresolvers import reverse
from agent.models import Agent


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        obj, created = Agent.objects.get_or_create(user=request.user)
        form_state = obj.form_state
        print 'users.accountadaptater - form_state ', form_state
        redirect_url = agent_form_redirect(form_state)
        print 'Entry in users.accountadaptater get_login_redirect_url'
        print 'URL DE REDIRECTION APRES get_login_redirect_url', redirect_url
        return reverse(redirect_url)
