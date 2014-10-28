# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse

# view imports
# from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView


# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from .forms import AgentForm
from .forms import AgentIdCardForm
from .forms import AgentAddressForm
from .forms import PoleEmploiForm
from .forms import CertificationsFormHelper
from .forms import AgentCertificationsForm
from .forms import AgentProCardForm

# Import the customized User model
from .models import Agent
from .models import AgentCertification
from .models import AgentIdCard
from .models import AgentAddress
from .models import AgentProCard
# from .models import AGENT_FORM_STATE


# Various imports
from django.http import HttpResponseRedirect
from extra_views import ModelFormSetView

# import messages
from django.contrib import messages


from allauth.account.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
def user_logged_in(request, user, **kwargs):
    print 'POST SIGNED UP SIGNAL RECEIVED'
    obj, created = Agent.objects.get_or_create(user=request.user)
    if created:
        print 'AGENT A ETE CREE', obj
    else:
        print 'AGENT EXISTE DEJA'
    # user signed up now send email
    # send email part - do your self


def AddAgentContextProcessor(self, request):
    try:
        user = self.user.request
        agent = user.Agent
        return {'agent': agent}
    except Agent.DoesNotExist:
        print"super pb"
        return {'marchepas': 'dededede'}


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


def agent_form_redirect(form_state):
    form_state = form_state
    print 'form_state', form_state
    for k in form_state.items():
        print 'cle', k[0]
        if k[1] == 0:
            print 'TROUVE CLE VIDE POUR REDIRECTION'
            if k[0] == 'NOM_PRENOM':
                redirect_url = 'users:update'
                break
            elif k[0] == 'AGENT':
                redirect_url = 'agent:~agent'
                break
            elif k[0] == 'COORDONNEES':
                redirect_url = 'agent:~agent_address'
                break
            elif k[0] == 'PAPIERS_IDENTITE':
                redirect_url = 'agent:~agent_id_card'
                break
            elif k[0] == 'CARTE_PRO':
                redirect_url = 'agent:~agent_pro_card'
                break
            elif k[0] == 'CERTIFICATIONS':
                redirect_url = 'agent:~agent_certification'
                break
        else:
            redirect_url = 'agent:~agent'

    print 'AGENT_FORN_REDIRECT_URL', redirect_url
    return redirect_url


def agent_form_state_update(request, obj, state):
        AGENT_FORM_STATE = obj.form_state
        AGENT_FORM_STATE[state] = 1
        Agent.objects.filter(user=request.user).update(form_state=AGENT_FORM_STATE)


class AgentCertificationsCreateView(LoginRequiredMixin, ModelFormSetView):
    template_name = 'agent/agent_certification_form.html'
    model = AgentCertification
    fields = ('certification', 'start_date', 'end_date', 'picture')
    can_delete = True
    extra = 3
    max_num = 3
    form_class = AgentCertificationsForm

    def get_queryset(self):
        queryset = AgentCertification.objects.filter(agent=self.request.user.agent)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AgentCertificationsCreateView, self).get_context_data(**kwargs)
        context['helper'] = CertificationsFormHelper
        return context

    def formset_valid(self, formset):
        self.user = self.request.user
        new_instances = formset.save(commit=False)
        for i in new_instances:
            i.agent = self.user.agent
        formset.save()
        obj = Agent.objects.get(user=self.request.user)
        agent_form_state_update(self.request, obj, 'CERTIFICATIONS')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("agent:~agent_certification",)


class AgentView(LoginRequiredMixin, UpdateView):

    form_class = AgentForm
    model = Agent
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj = Agent.objects.get(user=self.request.user)
        return obj

    def form_valid(self, form):
        form.save()
        obj = Agent.objects.get(user=self.request.user)
        agent_form_state_update(self.request, obj, 'AGENT')
        form_state = Agent.objects.get(user=self.request.user).form_state
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        redirect_url = agent_form_redirect(form_state)
        return HttpResponseRedirect(reverse(redirect_url))


class PoleEmploiUpdateView(LoginRequiredMixin, UpdateView):

    form_class = PoleEmploiForm
    model = Agent
    template_name = 'agent/poleemploi_form.html'

    def get_object(self, queryset=None):
        return Agent.objects.get(user=self.request.user)

    def form_valid(self, form):
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
            return HttpResponseRedirect(self.get_success_url())

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class AgentIdCardView(LoginRequiredMixin, UpdateView):

    form_class = AgentIdCardForm
    model = AgentIdCard
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentIdCard.objects.get_or_create(agent=self.request.user.agent)
        return obj

    def form_valid(self, form):
        form.save()
        obj = Agent.objects.get(user=self.request.user)
        agent_form_state_update(self.request, obj, 'PAPIERS_IDENTITE')
        form_state = Agent.objects.get(user=self.request.user).form_state
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        redirect_url = agent_form_redirect(form_state)
        return HttpResponseRedirect(reverse(redirect_url))


class AgentAddressView(LoginRequiredMixin, UpdateView):

    form_class = AgentAddressForm
    model = AgentAddress
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentAddress.objects.get_or_create(agent=self.request.user.agent)
        return obj

    def form_valid(self, form):
        form.save()
        obj = Agent.objects.get(user=self.request.user)
        agent_form_state_update(self.request, obj, 'COORDONNEES')
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        return HttpResponseRedirect(self.get_success_url())

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("agent:~agent_id_card",)


class AgentProCardView(LoginRequiredMixin, UpdateView):

    form_class = AgentProCardForm
    model = AgentProCard
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentProCard.objects.get_or_create(agent=self.request.user.agent)
        return obj

    def form_valid(self, form):
        form.save()
        obj = Agent.objects.get(user=self.request.user)
        agent_form_state_update(self.request, obj, 'CARTE_PRO')
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        return HttpResponseRedirect(self.get_success_url())

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("agent:~agent_pro_card",)
