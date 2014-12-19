from django.shortcuts import render
from django.views.generic.base import TemplateView
import datatableview
from datatableview.views import DatatableView

from agent.models import Agent
from agent.models import Certification 
from .models import Client
from .models import Selection 
from .forms import SelectionForm
from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic import CreateView

# Create your views here.
class ClientHomeView(TemplateView):
    template_name = 'client/home.html'



class SelectionView(LoginRequiredMixin, CreateView):

    form_class = SelectionForm
    model = Selection
    template_name = 'client/selection.html'

    #def get_object(self, queryset=None):
        #obj = Selection.objects.get_or_create(client=self.request.user.client.id)
        #return obj


# Datatable view.
class DDataTableView(DatatableView):
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
