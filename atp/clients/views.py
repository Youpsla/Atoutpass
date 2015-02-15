# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from agent.models import Agent
from agent.models import AreaDepartment
from .models import States
from .models import SelectionAgentsRelationship
from .models import Selection
from .models import Company
from .forms import SelectionForm
from .forms import AgentFilterForm
from .forms import CompanyForm
from braces.views import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count

from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.template import RequestContext

class CompanyAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Company
    template_name = 'client/company_add.html'
    form_class = CompanyForm
    success_url = reverse_lazy('clients:~client_home')
    success_message = "Les coordonnees de l'entreprise %(name)s ont bien ete creees"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('clients:~client_home'))


class CompanyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Company
    template_name = 'client/company_add.html'
    form_class = CompanyForm
    success_url = reverse_lazy('clients:~client_home')
    success_message = "Les coordonnees de %(name)s ont bien ete mises a jour"


# Create your views here.
class ClientLandingView(TemplateView):
    template_name = 'client/landing.html'

    def get_context_data(self, **kwargs):
        context = super(ClientLandingView, self).get_context_data(**kwargs)
        context['type'] = 'CL'
        return context


class ClientHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'client/home.html'


class SelectionAddView(LoginRequiredMixin, CreateView):
    form_class = SelectionForm
    model = Selection
    template_name = 'client/add_selection.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        # Change selection state to "created"
        return HttpResponseRedirect(reverse('clients:~selection_list_view'))


class SelectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Selection
    template_name = 'client/delete_selection.html'
    success_url = '/client/~client/selection/list'

    def get_object(self, queryset=None):
        obj = Selection.objects.get(owner=self.request.user, pk=self.kwargs['selectionid'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(SelectionDeleteView, self).get_context_data()
        context['selectionid'] = self.kwargs['selectionid']
        return context


#def selection_validate_view(request, pk):
    #print "PK : ", pk
    #selection = Selection.objects.get(id=pk)
    #selection.validate()
    #selection.save()
    #context_instance = RequestContext(request)
    ## if context_instance['company']:



class SelectionValidateView(LoginRequiredMixin, TemplateView):
    template_name = "client/selection_validate.html"

    def get_context_data(self, **kwargs):
        context = super(SelectionValidateView, self).get_context_data(**kwargs)
        #context['selectionid'] = self.kwargs.get('pk', None)
        selectionqs = Selection.objects.filter(pk=self.kwargs.get('pk', None)).prefetch_related('agents').annotate(num_agents=Count('agents'))
        context['selectionqs'] = selectionqs
        print selectionqs
        return context


def selection_add_view(request):
    form = Selection(request.POST or None)
    if form.is_valid():
        selection = form.save(commif=False)
        selection.client = request.user.client
        selection.save()
        form = AgentFilterForm()
        data = reverse('clients:~agent_list_json')
        # Create a list of agents associated vith the Selection Id. Returned necessary information for selection list init
        selection_agent_list = SelectionAgentsRelationship.objects.filter(selection=selection.id).values('agent__firstname', 'agent__lastname', 'agent__id')
        selection_agent_list = json.dumps(list(selection_agent_list), cls=DjangoJSONEncoder)

        return render(
            request,
            'client/datatable.html',
            {'form': form, 'data': data, 'selectionid': selection.id, 'selection_agent_list': selection_agent_list},
        )


@login_required
def selection_list_view(request, **kwargs):

    """
    Displays the selection list table.
    The data is loaded by the CLientListJsonView and rendered by the
    Datatables plugin via Javascript.
    """

    if request.method == 'POST' and request.is_ajax:
        # We need to create a copy of request.POST because it's immutable
        params = request.POST.copy()
        # Create the URL query string and strip the last '&' at the end.
        data = ('%s?%s' % (reverse('clients:~agent_list_json'), ''.join(
            ['%s=%s&' % (k, v) for k, v in params.iteritems()])))\
            .rstrip('&')
        return HttpResponse(json.dumps(data), content_type='application/json')

    if request.method == 'GET':
        data = reverse('clients:~selection_list_json')
        form = SelectionForm()

        return render(
            request,
            'client/selection_list.html',
            {'data': data, 'form': form},
        )


class SelectionListJsonView(LoginRequiredMixin, BaseDatatableView):
    model = Selection
    columns = ['pk', 'state', 'created', 'name', 'description', 'nb_agents', 'action']
    order_columns = ['pk', 'state', 'created', 'name', 'description', 'nb_agents']

    def render_column(self, row, column):
        if column == 'action':
            return """<a class="btn btn-primary btn-sm" href="%s">Agents</a>
                      <a class="btn btn-danger btn-sm" href="%s">Supprimer</a>""" % (reverse('clients:~agent_filter_view', kwargs={'selectionid': row.id}), reverse('clients:~selection_delete_view', kwargs={'selectionid': row.id}))
        elif column == 'state':
            state = States.objects.get(pk=row.state)
            return state.label
        elif column == 'created':
            return row.get_created_date_formated
        elif column == 'updated':
            return row.get_updated_date_formated
        else:
            return super(SelectionListJsonView, self).render_column(row, column)

    def get_initial_queryset(self):
        user = self.request.user
        """
        Return all Agents.
        """
        qs = Selection.objects.filter(owner=user).annotate(nb_agents=Count('agents'))
        return qs


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


@login_required
def agent_filter_view(request, **kwargs):

    """
    Displays the agent data table with filter options.
    The data is loaded by the AgentListJson view and rendered by the
    Datatables plugin via Javascript.
    """

    selectionid = kwargs['selectionid']
    get_object_or_404(Selection, owner=request.user, pk=selectionid)

    if request.method == 'POST' and request.is_ajax:
        # We need to create a copy of request.POST because it's immutable
        params = request.POST.copy()
        # Create the URL query string and strip the last '&' at the end.
        data = ('%s?%s' % (reverse('clients:~agent_list_json'), ''.join(
            ['%s=%s&' % (k, v) for k, v in params.iteritems()])))\
            .rstrip('&')
        return HttpResponse(json.dumps(data), content_type='application/json')

    if request.method == 'GET':
        form = AgentFilterForm()
        data = reverse('clients:~agent_list_json')
        # Create a list of agents associated vith the Selection Id. Returned necessary information for selection list init
        selection_agent_list = SelectionAgentsRelationship.objects.filter(selection=selectionid).values('agent__firstname', 'agent__lastname', 'agent__id')
        selection_agent_list = json.dumps(list(selection_agent_list), cls=DjangoJSONEncoder)

        return render(
            request,
            'client/datatable.html',
            {'form': form, 'data': data, 'selectionid': selectionid, 'selection_agent_list': selection_agent_list},
        )


class AgentListJsonView(LoginRequiredMixin, BaseDatatableView):
    model = Agent

    columns = ['id', 'firstname', 'lastname', 'area_department', 'actions']
    order_columns = ['id', '', '', '', '']
    max_display_length = 500

    def render_column(self, row, column):
        if column == 'area_department':
            qs = AreaDepartment.objects.filter(agentaddress__agent=row.id).values('num')
            if qs:
                for i in qs:
                    return i['num']
            else:
                return 0 
        elif column == 'actions':
            return """<button type="button" class="btn btn-info btn-sm bouton" data-agentid="%s" onclick="showagentdetailmodal('%s')" >Details</button>
                <button type="button" class="btn btn-primary btn-sm" data-agentid="%s" onclick="addtoselection('%s')">Ajouter</button>
        """ % (row.id, row.id, row.id, row.id)
        else:
            return super(AgentListJsonView, self).render_column(row, column)


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

        return qs
