from django.views.generic.base import TemplateView

from agent.models import Agent
from agent.models import AreaDepartment
from .models import Client
from .models import SelectionAgentsRelationship
from .models import Selection
from .forms import SelectionForm
from .forms import AgentFilterForm
from braces.views import LoginRequiredMixin
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import json
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import JsonResponse

from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.
class ClientHomeView(LoginRequiredMixin, TemplateView):
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


class SelectionListView(LoginRequiredMixin, ListView):
    model = Selection
    queryset = Selection.objects.for_user(2)
    print "HHHHHHHHHHHHHHHHHHHHH", queryset



@login_required
# def filter_view(request, selectionid):
def filter_view(request, **kwargs):
    user=request.user
    """
    Displays the agent data table with filter options.
    The data is loaded by the AgentListJson view and rendered by the
    Datatables plugin via Javascript.
    """

    if request.method == 'POST' and request.is_ajax:
        # We need to create a copy of request.POST because it's immutable
        params = request.POST.copy()
        
        # Create the URL query string and strip the last '&' at the end.
        data = ('%s?%s' % (reverse('clients:agent_list_json'), ''.join(
            ['%s=%s&' % (k, v) for k, v in params.iteritems()])))\
            .rstrip('&')

        return HttpResponse(json.dumps(data), content_type='application/json')

    if request.method == 'GET':
        selectionid = kwargs['selectionid']
        form = AgentFilterForm()
        data = reverse('clients:agent_list_json')
    # Create a list of agents associated vith the Selection Id. Returned necessary information for selection list init
        selection_agent_list = SelectionAgentsRelationship.objects.filter(selection=selectionid).values('agent__firstname', 'agent__lastname', 'agent__id')
        selection_agent_list = json.dumps(list(selection_agent_list), cls=DjangoJSONEncoder)

        return render(
            request,
            'client/datatable.html',
            {'form': form, 'data': data, 'selectionid': selectionid, 'selection_agent_list': selection_agent_list},
        )

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

def add_agent_to_selection(request):
    agentid = None
    if request.method == 'GET':
        agentid = request.GET['agentid']
        selectionid = request.GET['selectionid']
        a = Agent.objects.get(id=agentid)
        s = Selection.objects.get(pk=selectionid)

        # Check if agent is already in selection.
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


class AgentListJson(LoginRequiredMixin, BaseDatatableView):
    model = Agent

    columns = [ 'id', 'firstname', 'lastname','area_department', 'actions']
    order_columns = ['id', '', '', '','' ]
    max_display_length = 500

    def render_column(self, row, column):
        user = self.request.user
        if column == 'area_department':
            # return '%s' % row.agentaddress_set.address1
            qs = AreaDepartment.objects.filter(agentaddress__agent=row.id).values('num')
            if qs:
                for i in qs:
                    return i['num']
            else:
                print "NONONONONO"
                return 0 
        elif column == 'actions':
            return """<button type="button" class="btn btn-info btn-sm bouton" data-agentid="%s" onclick="showagentdetailmodal('%s')" >Details</button>
                <button type="button" class="btn btn-primary btn-sm" data-agentid="%s" onclick="addtoselection('%s')">Ajouter</button>
        """ % (row.id, row.id, row.id, row.id)
        else:
            return super(AgentListJson, self).render_column(row, column)


    def get_initial_queryset(self):
        """
        Return all Agents.
        """
        qs = Agent.objects.all().prefetch_related('agentaddress_set').select_related('agentaddress_set')
        return qs 

    def filter_queryset(self, qs):
        params = self.request.GET

        qualifications = params.get('qualifications', '')
        if qualifications:
            qs = qs.filter(qualifications__in=qualifications)
            
        has_car = params.get('has_car', '')
        if has_car:
            qs = qs.filter(agentvarious__has_car=True)
        
        area_department = params.get('area_department', '')
        if area_department:
            qs = qs.filter(agentaddress__area_department=area_department)

        # print "queryset :", qs
        return qs
