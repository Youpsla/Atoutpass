# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse

# view imports
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.views.generic.base import TemplateView


# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from .forms import AgentForm
from .forms import AgentIdCardForm
from .forms import AgentAddressForm
from .forms import CertificationsFormHelper
from .forms import AgentCertificationsForm
from .forms import AgentProCardForm
from .forms import AgentVariousForm
from .forms import AgentQualificationsForm
from .forms import AgentQualificationsFormHelper

# Import the customized User model
from .models import Agent
from .models import AgentCertification
from .models import AgentIdCard
from .models import AgentAddress
from .models import AgentProCard
from .models import AgentQualification
from .models import AgentVarious


# Various imports
from django.http import HttpResponseRedirect
from extra_views import ModelFormSetView
from django.shortcuts import get_object_or_404

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

from phantom_pdf import render_to_pdf
from django.http import HttpResponse


def testpdf(request):
    basename = 'dedede'
    return render_to_pdf(request, basename)

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

    if form_state['NOM_PRENOM'] == 0:
        redirect_url = 'users:update'
    elif form_state['AGENT'] == 0:
        redirect_url = 'agent:~agent'
    elif form_state['COORDONNEES'] == 0:
        redirect_url = 'agent:~agent_address'
    elif form_state['PAPIERS_IDENTITE'] == 0:
        redirect_url = 'agent:~agent_id_card'
    elif form_state['CARTE_PRO'] == 0:
        redirect_url = 'agent:~agent_pro_card'
    elif form_state['CERTIFICATIONS'] == 0:
        redirect_url = 'agent:~agent_certification'
    elif form_state['DIVERS'] == 0:
        redirect_url = 'agent:~agent_various'
    else:
        redirect_url = 'agent:~agent_home'

    return redirect_url


def agent_form_state_update(request, obj, state):
        AGENT_FORM_STATE = obj.form_state
        AGENT_FORM_STATE[state] = 1
        Agent.objects.filter(user=request.user).update(form_state=AGENT_FORM_STATE)


class AgentFormValidMixin(LoginRequiredMixin, UpdateView):
    """
    This Mixin:
    - update AGENT_FORM_STATE
    - determine redirect_url using agent_form_redirect()
    """

    def form_valid(self, form):

        # Update AGENT_FORM_STATE
        path = self.request.META['PATH_INFO']
        var = path.split('/')[2]

        if var == '~update':
            FORM_STATE = 'NOM_PRENOM'
        if var == '~agent':
            FORM_STATE = 'AGENT'
        elif var == '~agent_address':
            FORM_STATE = 'COORDONNEES'
        elif var == '~agent_id_card':
            FORM_STATE = 'PAPIERS_IDENTITE'
        elif var == '~agent_pro_card':
            FORM_STATE = 'CARTE_PRO'
        elif var == '~agent_pro_card_qualifications':
            FORM_STATE = 'QUALIFICATIONS'
        elif var == '~agent_certifications':
            FORM_STATE = 'CERTIFICATIONS'
        elif var == '~agent_various':
            FORM_STATE = 'DIVERS'

        # Save Form
        form.save()

        # Update AGENT_FORM_STATE in database. Mandatory because Django-jsonfield doesnt implement Postgresql direct key lookup
        obj = Agent.objects.get(user=self.request.user)
        agent_form_state_update(self.request, obj, FORM_STATE)

        # Retrieve form_state from DB
        form_state = Agent.objects.get(user=self.request.user).form_state
        agent_state = Agent.objects.get(user=self.request.user).state
        print 'Agent State : ', agent_state

        # Set redirect_url by passing form_state to agent_form_redirect
        redirect_url = agent_form_redirect(form_state)

        # Check if agent form is complete
        if 0 in form_state.values():
            print 'Le formulaire est INCOMPLET'
            messages.add_message(self.request, messages.ERROR, u'Votre Profil est incomplet. Veuillez renseigner les formulaires des onglets encore en rouge.')
        else:
            print 'Le formulaire est COMPLET'
            messages.add_message(self.request, messages.SUCCESS, u'Merci. Votre profil va maintenant etre communiqué a un conseiller. Vous serez contacté dans les plus brefs délais')


        # Update messages
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')

        # Redirect to redirect_url
        return HttpResponseRedirect(reverse(redirect_url))


class AgentHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'agent/home.html'


class AgentLandingView(TemplateView):
    template_name = 'agent/landing.html'

    def get_context_data(self, **kwargs):
        context = super(AgentLandingView, self).get_context_data(**kwargs)
        context['type'] = 'agent'
        return context


class AgentProfileReadonlyView(LoginRequiredMixin, TemplateView):
    template_name = 'agent/profile_readonly.html'

    def get_context_data(self, **kwargs):
        context = super(AgentProfileReadonlyView, self).get_context_data(**kwargs)
        cert = AgentCertification.objects.filter(agent=self.request.user.agent)
        qual = AgentQualification.objects.filter(agent=self.request.user.agent)
        context['cert'] = cert
        context['qual'] = qual
        return context


class AgentCertificationsCreateView(LoginRequiredMixin, ModelFormSetView):
    template_name = 'agent/agent_certification_form.html'
    model = AgentCertification
    fields = ('certification', 'start_date', 'end_date', 'picture')
    can_delete = True
    extra = 3
    max_num = 3
    form_class = AgentCertificationsForm

    def get_queryset(self):
        queryset = AgentCertification.objects.filter(agent=self.request.user.users_agent)
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
        # Retrieve form_state from DB
        form_state = Agent.objects.get(user=self.request.user).form_state

        # Set redirect_url by passing form_state to agent_form_redirect
        redirect_url = agent_form_redirect(form_state)

        # Update messages
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        # Check if agent form is complete
        if 0 in form_state.values():
            print 'Le formulaire est INCOMPLET'
            messages.add_message(self.request, messages.ERROR, u'Votre Profil est incomplet. Veuillez renseigner les formulaires des onglets encore en rouge.')
        else:
            print 'Le formulaire est COMPLET'
            messages.add_message(self.request, messages.SUCCESS, u'Merci. Votre profil va maintenant etre communiqué a un conseiller. Vous serez contacté dans les plus brefs délais')

        return HttpResponseRedirect(reverse(redirect_url))


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
        obj, created = AgentIdCard.objects.get_or_create(agent=self.request.user.users_agent)
        return obj


class AgentAddressView(AgentFormValidMixin):

    form_class = AgentAddressForm
    model = AgentAddress
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentAddress.objects.get_or_create(agent=self.request.user.users_agent)
        return obj


class AgentQualificationCreateView(LoginRequiredMixin, ModelFormSetView):
    template_name = 'agent/agent_qualification_form.html'
    model = AgentQualification
    fields = ('qualification', 'start_date', 'end_date')
    can_delete = True
    extra = 3
    max_num = 3
    form_class = AgentQualificationsForm

    def get_queryset(self):
        queryset = AgentQualification.objects.filter(agent=self.request.user.users_agent)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AgentQualificationCreateView, self).get_context_data(**kwargs)
        context['helper'] = AgentQualificationsFormHelper
        return context

    def formset_valid(self, formset):
        self.user = self.request.user
        new_instances = formset.save(commit=False)
        for i in new_instances:
            i.agent = self.user.agent
        formset.save()
        obj = Agent.objects.get(user=self.request.user)
        agent_form_state_update(self.request, obj, 'QUALIFICATIONS')
        # Retrieve form_state from DB
        form_state = Agent.objects.get(user=self.request.user).form_state

        # Set redirect_url by passing form_state to agent_form_redirect
        redirect_url = agent_form_redirect(form_state)

        # Update messages
        messages.add_message(self.request, messages.INFO, u'Informations sauvegardées avec succès.')
        # Check if agent form is complete
        if 0 in form_state.values():
            print 'Le formulaire est INCOMPLET'
            messages.add_message(self.request, messages.ERROR, u'Votre Profil est incomplet. Veuillez renseigner les formulaires des onglets encore en rouge.')
        else:
            print 'Le formulaire est COMPLET'
            messages.add_message(self.request, messages.SUCCESS, u'Merci. Votre profil va maintenant etre communiqué a un conseiller. Vous serez contacté dans les plus brefs délais')

        return HttpResponseRedirect(reverse(redirect_url))

class AgentProCardView(AgentFormValidMixin):

    form_class = AgentProCardForm
    model = AgentProCard
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentProCard.objects.get_or_create(agent=self.request.user.users_agent)
        return obj



class AgentVariousView(AgentFormValidMixin):

    form_class = AgentVariousForm
    model = AgentVarious
    template_name = 'agent/profile.html'

    def get_object(self, queryset=None):
        obj, created = AgentVarious.objects.get_or_create(agent=self.request.user.users_agent)
        return obj


# PDF GENERATION
from easy_pdf.views import PDFTemplateView
from eventlog.models import log


class HelloPDFView(PDFTemplateView):
    template_name = "agent/agent_pdf.html"

    def get_context_data(self, **kwargs):
        context = super(HelloPDFView, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )
        agent = Agent.objects.get(user=self.request.user)
        agent_id_card = AgentIdCard.objects.get(agent=agent)
        address = AgentAddress.objects.get(agent=agent)
        context['id_card'] = agent_id_card
        context['agent'] = agent
        context['address'] = address
        print agent.agentprocard_set.all()
        log(
                user=self.request.user,
                action="EXPORT DU DOSSIER CANDIDAT",
                extra={
                    "Agent": agent.firstname,
                }
            )
        return context

import json
from django.db.models import Prefetch
from django.core import serializers
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
class AgentDetailModal(LoginRequiredMixin, DetailView):
    template_name = 'agent/agent_detail_modal.html'
    model = Agent


    def render_to_response(self, context, **response_kwargs):
        #agent = Agent.objects.filter(pk=self.kwargs['pk']).prefetch_related(
                #Prefetch('agentaddress_set', to_attr="dede"),
                #Prefetch('agentvarious_set', to_attr="dodo"),
                #Prefetch('idcard', to_attr="didi"))
        #print agent[0].dede[0].address1
        #print agent[0].didi[0].id_card_type
        pk=self.kwargs['pk']
        agent = Agent.objects.select_related(
                'agentaddress',
                'agentvarious',
                'idcard',
                'procard',
                # ).filter(pk=pk)
                ).get(pk=pk)
        agent_js = serializers.serialize('json', [agent])
        try:
            aidcard = agent.idcard.get()
            aidcard_js = serializers.serialize('json', [aidcard])
        except ObjectDoesNotExist:
            aidcard_js = json.dumps({})
            aidcard = ''
        try:
            address = agent.agentaddress_set.get()
            address_js = serializers.serialize('json', [address])
        except ObjectDoesNotExist:
            address_js = json.dumps({})
            address = ''
        try:
            procard = agent.procard.get()
            procard_js = serializers.serialize('json', [procard])
        except ObjectDoesNotExist:
            procard_js = json.dumps({})
            procard = ''
        try:
            various = agent.agentvarious_set.get()
            various_js = serializers.serialize('json', [various])
        except ObjectDoesNotExist:
            various_js = json.dumps({})
            various = ''
        dic = {'agent': agent_js,
               'address': address_js,
               'idcard': aidcard_js,
               "procard": procard_js,
               'various': various_js,
               'idcard': aidcard_js}
        print dic
        print 'DEDE: ', json.dumps(dic, indent=4)

        data = [agent_js, address_js, aidcard_js, procard_js, various_js]
        #for i in data:
            #j = serializers.serialize(i)
            #data_json.append()
        # agent_serialized = serializers.serialize('json', data)
        # print agent_serialized
        # return JsonResponse(agent_serialized, safe=False)
        # return JsonResponse(json.dumps(data), safe=False)
        return JsonResponse({'agent': agent_js,
               'address': address_js,
               'idcard': aidcard_js,
               'procard': procard_js,
               'various': various_js,
               'idcard': aidcard_js}, safe=False)


