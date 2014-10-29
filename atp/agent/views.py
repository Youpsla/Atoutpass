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
        if 0 in AGENT_FORM_STATE.values():
            print 'ca passe dedans'
            messages.add_message(request, messages.ERROR, u'Votre Profil est incomplet. Veuillez renseigner les formulaires des onglets encore en rouge.')
        else:
            pass
        Agent.objects.filter(user=request.user).update(form_state=AGENT_FORM_STATE)


def agent_get_current_form(path_info):
    pass


class AgentFormValidMixin(LoginRequiredMixin, UpdateView):
    """
    This Mixin:
    - update AGENT_FOMR_STATE
    - determine redirect_url using agent_form_redirect()
    """

    def form_valid(self, form):
        path = self.request.META['PATH_INFO']
        var = path.split('/')[2]

        if var == '~agent':
            FORM_STATE = 'AGENT'
        elif var == '~agent_address':
            FORM_STATE = 'COORDONNEES'
        elif var == '~agent_id_card':
            FORM_STATE = 'PAPIERS_IDENTITE'
        elif var == '~agent_pro_card':
            FORM_STATE = 'CARTE_PRO'
        elif var == '~agent_certifications':
            FORM_STATE = 'CERTIFICATIONS'
       
        # Save Form
        form.save()

        # Update AGENT_FORM_STATE in database
        obj = Agent.objects.get(user=self.request.user)
        agent_form_state_update(self.request, obj, FORM_STATE)

        # Determine redirect_url by fetching form_state in the DB
        form_state = Agent.objects.get(user=self.request.user).form_state
        redirect_url = agent_form_redirect(form_state)

        # Update messages
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')

        # Redirect to redirect_url
        return HttpResponseRedirect(reverse(redirect_url))


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

from django.utils.decorators import method_decorator

def agent_profil_completed_decorator(dede):
    print dede
    print 'yahooooooooooooooooooooooo'


class AgentView(AgentFormValidMixin):

    form_class = AgentForm
    model = Agent
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj = Agent.objects.get(user=self.request.user)
        return obj


class AgentIdCardView(AgentFormValidMixin):

    form_class = AgentIdCardForm
    model = AgentIdCard
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentIdCard.objects.get_or_create(agent=self.request.user.agent)
        return obj


class AgentAddressView(AgentFormValidMixin):

    form_class = AgentAddressForm
    model = AgentAddress
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentAddress.objects.get_or_create(agent=self.request.user.agent)
        return obj


class AgentProCardView(AgentFormValidMixin):

    form_class = AgentProCardForm
    model = AgentProCard
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentProCard.objects.get_or_create(agent=self.request.user.agent)
        return obj
