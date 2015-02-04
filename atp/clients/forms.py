# -*- coding: utf-8 -*-
from django import forms
from .models import Selection
from agent.models import AreaDepartment
from agent.models import Qualification
from agent.models import AgentAddress
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Submit
from crispy_forms.layout import Reset 
from crispy_forms.layout import Field
from crispy_forms.bootstrap import FormActions


# Register your models here.

class SelectionForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = Selection

        exclude = ('client', 'start_date', 'last_modified', 'state')

    def __init__(self, *args, **kwargs):
        super(SelectionForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['description'].required = True
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form = 'SELECTION'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('clients:~add_selection')
        self.helper.layout = Layout(
            Fieldset(u'1) Indiquez le nom et la description de votre selection',
                     'name', 'description'),
            )
        self.helper.layout.append(Submit('save', 'Valider'))

#class SearchForm(forms.Form):
    #def __init__(self, *args, **kwargs):
        #super(SearchForm, self).__init__(*args, **kwargs)
        ## self.fields['qualifications'].required = True
        #self.helper = FormHelper()
        #self.helper.form = 'SEARCH'
        #self.helper.form_action = reverse('clients:~clients_datatable')
        #self.helper.layout.append(Submit('save', 'Valider'))

class AgentFilterForm(forms.Form):

    AREA_DEPARTMENT_CHOICES = AreaDepartment.objects.filter().values_list('id','name')

    qualifications = forms.ModelChoiceField(
            queryset=Qualification.objects.all(), required=False,
            # widget=forms.CheckboxSelectMultiple(),
            widget=forms.RadioSelect(),
            empty_label=None,)
    has_car = forms.ChoiceField(
            # choices=((True,'Oui'), (False,'Non')),
            choices=((True,'Oui'),),
            widget=forms.RadioSelect(),
            required=False,
            label=u'Possède une voiture')
    area_department = forms.ChoiceField(
            choices=AREA_DEPARTMENT_CHOICES,
            widget=forms.Select(),
            required=False,
            label=u'Département')

    def __init__(self, *args, **kwargs):
        super(AgentFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'filter_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'

        self.helper.layout = Layout(
            Field('qualifications'),
            Field('area_department'),
            Field('has_car'),
            FormActions(
                Submit('submit', 'Rechercher'),
                Reset('reset', 'Effacer')
                ),
            )

