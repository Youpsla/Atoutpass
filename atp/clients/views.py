from django.shortcuts import render
from django.views.generic.base import TemplateView
import datatableview
from datatableview.views import DatatableView

from agent.models import Agent
from agent.models import Certification 
from .models import Client
from .models import SelectionAgentsRelationship
from .models import Selection 
from .forms import SelectionForm
from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse

# Create your views here.
class ClientHomeView(TemplateView):
    template_name = 'client/home.html'



class SelectionView(LoginRequiredMixin, CreateView):

    form_class = SelectionForm
    model = Selection
    template_name = 'client/selection.html'

    def form_valid(self, form):
        form.instance.client = Client.objects.get(user=self.request.user)
        form.save()
        return HttpResponseRedirect(reverse('clients:~client_home'))


    #def get_object(self, queryset=None):
        #obj = Selection.objects.get_or_create(client=self.request.user.client.id)
        #return obj


# Datatable view.
class DataTableView(DatatableView):
    model = Agent 
    template_name = 'client/datatable.html'
    datatable_options = {
            'columns' : [
                'firstname',
                'lastname',
                ("Certification", 'agent__certifications', 'get_agent_certifications'),
                ("Id", 'get_id'),
                ]
            }
    def get_agent_certifications(self, instance, *args, **kwargs):
        return ", ".join([Certification.long_name for Certification in instance.certifications.all()])

import json
def add_agent_to_selection(request):
    agentid = None
    if request.method == 'GET':
        agentid = request.GET['agentid']
        print 'AGENT_ID : ', agentid
        a = Agent.objects.get(id=agentid)
        s = Selection.objects.get(id=14)
        if SelectionAgentsRelationship.objects.filter(agent=a, selection=s).exists():
            print "Agent %s already in selection %s" % (a.id, s.id)
            payload = {'duplicate': 'ok'}
            return HttpResponse(json.dumps(payload), content_type="application/json")
        else:
            s.agents.add(a)
            print "Agent %s added to selection %s" % (a.id, s.id)
            payload = {'added': 'ok'}
            return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_agent_from_selection(request):
    agentid = None
    if request.method == 'GET':
        agentid = request.GET['agentid']
        a = Agent.objects.get(id=agentid)
        s = Selection.objects.get(id=14)
        s.agents.remove(a)
    return HttpResponse()
