# -*- coding: utf-8 -*-


from allauth.account.adapter import DefaultAccountAdapter
from agent.views import agent_form_redirect
from django.core.urlresolvers import reverse
from agent.models import Agent


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        if request.user.type == 'AG':
            obj = Agent.objects.get(user=request.user)
            form_state = obj.form_state
            redirect_url = agent_form_redirect(form_state)
        elif request.user.type == 'CL':
            redirect_url = 'clients:~client_home'
        return reverse(redirect_url)
