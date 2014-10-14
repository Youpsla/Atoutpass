from django.shortcuts import render

# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse

# view imports
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import CreateView

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from .forms import AgentForm
from .forms import PoleEmploiForm
from .forms import CertificationsFormHelper
from .forms import AgentCertificationsForm

# Import the customized User model
from .models import Agent
from .models import PoleEmploi
from .models import Certification
from .models import AgentCertification

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from datetime import date


def AddAgentContextProcessor(request):
    try:
        user = self.user.request
        agent = user.Agent
        return {'agent' : agent}
    except Agent.DoesNotExist:
        print"super pb"
        return {'marchepas':'dededede'}





# import the logging library
import logging

# Get an instance of a logger
# logger = logging.getLogger(__name__)
logger = logging.getLogger('agent')



class AgentDetailView(LoginRequiredMixin, DetailView):
    model = Agent
    # These next two lines tell the view to index lookups by username
    #slug_field = "username"
    #slug_url_kwarg = "username"

    def get_object(self):
        # Only get the User record for the user making the request
        self.user_id = User.objects.get(username=self.request.user.username)
        print 'User: ' + str(self.user_id.id)
        # return Agent.objects.get(user_ptr=str(self.user_id.id))
        return Agent.objects.filter(user=str(self.user_id.id))

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


from datetimewidget.widgets import DateWidget
import pdb
from extra_views import ModelFormSetView
class AgentCertificationsCreateView(LoginRequiredMixin, ModelFormSetView):
    template_name = 'agent/agent_certification_form.html'
    model = AgentCertification
    fields = ("start_date","certification")
    can_delete = True
    extra = 3
    max_num = 3
    form_class = AgentCertificationsForm


    def get_context_data(self,**kwargs):
        context = super(AgentCertificationsCreateView, self).get_context_data(**kwargs)
        context['helper'] = CertificationsFormHelper
        return context

    def formset_valid(self, formset):
        self.user = self.request.user
        new_instances = formset.save(commit=False)
        for i in new_instances:
            i.agent = self.user.agent
        # pdb.set_trace()
        for form in formset.forms:
            form.agent = self.user.agent
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("agent:create_agentcertifications",)
    #def formset_save(self, user=None):
        #self.myobject = super(AgentCertificationsCreateView, self).save(commit=False)
        #self.myobject.agent_id = self.request.user.agent.id
        #self.myobject.save()




#class AgentCertificationsCreateView(LoginRequiredMixin, CreateView):

    #model = Agent
    #form_class = CertificationsForm

    #def form_valid(self, form):
            #obj = form.save(commit=False)
            #obj.user = self.request.user
            #obj.save()
            #return HttpResponseRedirect(self.get_success_url())

    #def form_invalid(self, form):
        #return self.form_invalid(get_context_data(form=form, formset=formset))

    #def get(self, request, *args, **kwargs):
        #"""
        #Handles GET requests and instantiates blank versions of the form
        #and its inline formsets.
        #"""
        #self.object = None
        #form_class = self.get_form_class()
        #form = self.get_form(form_class)
        ## formset = CertificationFormSet()
        #formset = CertificationFormSet(queryset=AgentCertification.objects.none())
        #return self.render_to_response(
            #self.get_context_data(form=form,
                                    #formset=formset))

    #def post(self, request, *args, **kwargs):
            #"""
            #Handles POST requests, instantiating a form instance and its inline
            #formsets with the passed POST variables and then checking them for
            #validity.
            #"""
            #self.object = None
            #form_class = self.get_form_class()
            #form = self.get_form(form_class)
            #role_form = CertificationFormSet(self.request.POST)
            #formset = CertificationFormSet(request.POST)
            #form_valid = form.is_valid()
            #formset_valid = formset.is_valid()
            #if form_valid and formset_valid:
                #self.form_validsave()
                #certifications = formset.save(commit=False)
                #for i in certifications:
                    #i.agent = self.form_classi.save
                #formset.save_m2m()
                #return self.form_valid()
            #else:
                #return self.form_invalid(form, formset)

    ### send the user back to their own page after a successful update
    #def get_success_url(self):
        #return reverse("agent:create",
                       #kwargs={"username": self.request.user.username})


class AgentCreateView(LoginRequiredMixin, CreateView):

    form_class = AgentForm
    model = Agent

    def form_valid(self, form):
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
            return HttpResponseRedirect(self.get_success_url())

    ## send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("agent:create",
                       kwargs={"username": self.request.user.username})


from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView
from extra_views.generic import GenericInlineFormSet



class AgentUpdateView(LoginRequiredMixin, UpdateView):

    form_class = AgentForm
    model = Agent

    def get_object(self, queryset=None):
        logger.debug('User trouve dans le contexte : %s' % (self.request.user))
        print self.request.user
        return Agent.objects.get(user=self.request.user)

    def form_valid(self, form):
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
            return HttpResponseRedirect(self.get_success_url())

    ## send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("agent:update",
                       )

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

    ## send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})
