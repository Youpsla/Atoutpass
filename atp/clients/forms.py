# -*- coding: utf-8 -*-
from django import forms
from .models import Selection
from .models import Company
from agent.models import AreaDepartment
from agent.models import Qualification
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from crispy_forms.layout import Reset
from crispy_forms.layout import Field
from crispy_forms.layout import Fieldset
from crispy_forms.bootstrap import FormActions


# Register your models here.

class SelectionForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = Selection

        exclude = ('owner', 'start_date', 'last_modified', 'state')

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
            Field('name'),
            Field('description'),
            )
        self.helper.layout.append(Submit('save', 'Valider'))


class AgentFilterForm(forms.Form):

    AREA_DEPARTMENT_CHOICES = AreaDepartment.objects.filter().values_list('id', 'name')

    qualifications = forms.ModelChoiceField(
        queryset=Qualification.objects.all(), required=False,
        # widget=forms.CheckboxSelectMultiple(),
        widget=forms.RadioSelect(),
        empty_label=None,)
    has_car = forms.ChoiceField(
        # choices=((True,'Oui'), (False,'Non')),
        choices=((True, 'Oui'),),
        widget=forms.RadioSelect(),
        required=False,
        label=u'Possède une voiture')
    area_department = forms.ChoiceField(
        choices=AREA_DEPARTMENT_CHOICES,
        widget=forms.Select(),
        required=False,
        label=u'Département',
        initial=76)

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


class CompanyForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = Company

        exclude = ('user', 'created', 'updated')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['name'].help_text = """Raison sociale, nom de l'association ..."""
        self.fields['phonenumber'].required = True
        self.fields['siret'].required = True
        self.fields['address1'].required = True
        self.fields['zipcode'].required = True
        self.fields['city'].required = True
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-5'
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.layout = Layout(
            Fieldset("""Nom de l'entreprise""",
                     'name'
                     ),
            Fieldset("""Telephone""",
                     'phonenumber',
                     ),
            Fieldset("""Adresse postale""",
                     'address1',
                     'address2',
                     'zipcode',
                     'city'),
            Fieldset("""Divers""",
                     'siret',
                     'ape',
                     'vat_number'),
            )
        self.helper.layout.append(Submit('save', 'Valider'))
