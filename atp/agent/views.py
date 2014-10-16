# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse

# view imports
# from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
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
from .models import AgentCertification

# Various imports
from django.http import HttpResponseRedirect
from extra_views import ModelFormSetView
# import pdb


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


class AgentCertificationsCreateView(LoginRequiredMixin, ModelFormSetView):
    template_name = 'agent/agent_certification_form.html'
    model = AgentCertification
    fields = ("start_date", "certification")
    can_delete = True
    extra = 3
    max_num = 3
    form_class = AgentCertificationsForm

    def get_context_data(self, **kwargs):
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
    # def formset_save(self, user=None):
        # self.myobject = super(AgentCertificationsCreateView, self).save(commit=False)
        # self.myobject.agent_id = self.request.user.agent.id
        # self.myobject.save()


class AgentCreateView(LoginRequiredMixin, CreateView):

    form_class = AgentForm
    model = Agent

    def form_valid(self, form):
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
            return HttpResponseRedirect(self.get_success_url())

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("agent:create",
                       kwargs={"username": self.request.user.username})


class AgentUpdateView(LoginRequiredMixin, UpdateView):

    form_class = AgentForm
    model = Agent

    def get_object(self, queryset=None):
        print self.request.user
        return Agent.objects.get(user=self.request.user)

    def form_valid(self, form):
            obj = form.save(commit=False)
            obj.user = self.request.user
            obj.save()
            return HttpResponseRedirect(self.get_success_url())

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("agent:update",)


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
