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
    print 'form_sate.items() type', type(form_state)

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
    else:
        redirect_url = 'agent:~agent'

    return redirect_url


def agent_form_state_update(request, obj, state):
        AGENT_FORM_STATE = obj.form_state
        AGENT_FORM_STATE[state] = 1
        Agent.objects.filter(user=request.user).update(form_state=AGENT_FORM_STATE)


def agent_get_current_form(path_info):
    pass


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
        print 'fffffff', var

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
        elif var == '~agent_certifications':
            FORM_STATE = 'CERTIFICATIONS'

        # Save Form
        form.save()

        # Update AGENT_FORM_STATE in database. Mandatory because Djqngo-jsonfield doesnt implement Postgresql direct key lookup
        obj = Agent.objects.get(user=self.request.user)
        agent_form_state_update(self.request, obj, FORM_STATE)

        # Retrieve form_state from DB
        form_state = Agent.objects.get(user=self.request.user).form_state

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
        # Retrieve form_state from DB
        form_state = Agent.objects.get(user=self.request.user).form_state

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



import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

# Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % \
                    (sUrl, mUrl))
    return path

#import StringIO
#from cgi import escape
#from xhtml2pdf import pisa
#from django.http import HttpResponse
#from django.template.response import TemplateResponse
#from django.views.generic import TemplateView

#class PDFTemplateResponse(TemplateResponse):

    #def generate_pdf(self, retval):

        #html = self.content

        #result = StringIO.StringIO()
        #rendering = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)

        #if rendering.err:
            #return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
        #else:
            #self.content = result.getvalue()

    #def __init__(self, *args, **kwargs):
        #super(PDFTemplateResponse, self).__init__(*args, mimetype='application/pdf', **kwargs)
        #self.add_post_render_callback(self.generate_pdf)


#class PDFTemplateView(TemplateView):
    #response_class = PDFTemplateResponse

#class HelloPDFView(PDFTemplateView):
    #template_name = "agent/agent_pdf.html"

from easy_pdf.views import PDFTemplateView

class HelloPDFView(PDFTemplateView):
    template_name = "agent/agent_pdf.html"

    def get_context_data(self, **kwargs):
        context = super(HelloPDFView, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )
        print self.request.user
        agent = Agent.objects.get(user = self.request.user)
        agent_id_card = AgentIdCard.objects.get(agent = agent)
        context['id_card'] = agent_id_card
        return context

    #def generate_pdf(request, type):
        ## Prepare context
        #data = {}
        #data['farmer'] = 'Old MacDonald'
        #data['animals'] = [('Cow', 'Moo'), ('Goat', 'Baa'), ('Pig', 'Oink')]

        ## Render html content through html template with context
        #template = get_template('lyrics/oldmacdonald.html')
        #html  = template.render(Context(data))

        ## Write PDF to file
        #file = open(os.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
        #pisaStatus = pisa.CreatePDF(html, dest=file,
                #link_callback = link_callback)

        ## Return PDF document through a Django HTTP response
        #file.seek(0)
        #pdf = file.read()
        #file.close()            # Don't forget to close the file handle
        #return HttpResponse(pdf, mimetype='application/pdf')
