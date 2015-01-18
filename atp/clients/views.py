from django.views.generic.base import TemplateView
from datatableview.views import DatatableView

from agent.models import Agent
from agent.models import Certification
from .models import Client
from .models import SelectionAgentsRelationship
from .models import Selection
from .forms import SelectionForm
from braces.views import LoginRequiredMixin
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import json


# Create your views here.
class ClientHomeView(TemplateView):
    template_name = 'client/home.html'


class SelectionView(LoginRequiredMixin, CreateView):
    form_class = SelectionForm
    model = Selection
    template_name = 'client/add_selection.html'

    def form_valid(self, request):
        form.instance.client = Client.objects.get(user=self.request.user)
        # Create an instance for updating state field later
        new_selection = form.save(commit=False)
        new_selection.save()
        # Change selection state to "created"
        new_selection.create()
        new_selection.save()
        return HttpResponseRedirect(reverse('clients:~list_selection'))


class SelectionListView(DatatableView):
    model = Selection
    template_name = 'client/list_selection.html'

    datatable_options = {
        'columns': [
            'id',
            'start_date',
            'name',
            'description',
            ("Etat", 'state__label'),
            "Action", 'add_action_button',
            ]
        }


# Datatable view.
class DataTableView(DatatableView):
    model = Agent 
    template_name = 'client/datatable.html'
    datatable_options = {
        #'structure_template': "datatableview/bootstrap_structure.html",
        'columns': [
            'firstname',
            'lastname',
            ("Certification", 'agent__certifications', 'get_agent_certifications'),
            ("Id", 'get_id'),
        ]
        }

    def get_agent_certifications(self, instance, *args, **kwargs):
        return ", ".join([Certification.long_name for Certification in instance.certifications.all()])

    def get_context_data(self, **kwargs):
        context = super(DatatableView, self).get_context_data(**kwargs)
        selectionid = self.request.GET.get('selectionid')
        print 'SELECTION ID : ', selectionid
        context['selectionid'] = selectionid
        agentids = SelectionAgentsRelationship.objects.filter(selection=selectionid)
        agents = [] 
        for i in agentids:
            agent = {'id': i.agent.id, 'firstname':i.agent.firstname, 'lastname': i.agent.lastname}
            agents.append(agent)
            print i.agent.firstname
        jsagents = json.dumps(agents)
        print agents
        print jsagents
        context['agents'] = jsagents
        return context


def retrieve_selection_agents(request):
    if request.method == 'GET':
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

from django.http import JsonResponse
def add_agent_to_selection(request):
    agentid = None
    if request.method == 'GET':
        agentid = request.GET['agentid']
        selectionid = request.GET['selectionid']
        a = Agent.objects.get(id=agentid)
        s = Selection.objects.get(id=selectionid)

        #
        # Check if agent is already in selection.
        #
        if SelectionAgentsRelationship.objects.filter(agent=a, selection=s).exists():
            print "Agent %s is already in selection %s" % (agentid, selectionid)
            payload = {'duplicate': 'ok'}
            return JsonResponse(payload)
        else:
            s.agents.add(a)
            print "Agent %s added in selection %s" % (agentid, selectionid)
            firstname = a.firstname
            lastname = a.lastname
            payload = {'added': 'ok', 'firstname': firstname, 'lastname': lastname}
            return JsonResponse(payload)


def remove_agent_from_selection(request):
    agentid = None
    if request.method == 'GET':
        agentid = request.GET['agentid']
        selectionid = request.GET['selectionid']
        a = Agent.objects.get(id=agentid)
        s = Selection.objects.get(id=selectionid)
        s.agents.remove(a)
    print "Agent %s deleted from selection %s" % (agentid, selectionid)
    return HttpResponse()
