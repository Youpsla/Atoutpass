# -*- coding: utf-8 -*-
from django import forms

from .models import Agent
from .models import AgentCertification
from .models import Certification

from datetimewidget.widgets import DateWidget
from datetimewidget.widgets import DateTimeWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from crispy_forms.layout import MultiField
from crispy_forms.layout import Field
from crispy_forms.layout import Div
from crispy_forms.bootstrap import Tab
from crispy_forms.bootstrap import Accordion
from crispy_forms.bootstrap import AccordionGroup
from django.core.urlresolvers import reverse



class AgentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        self.fields['birthdate'].required = True
        self.fields['address1'].required = True
        self.fields['birthplace'].required = True
        self.fields['zipcode'].required = True
        self.fields['city'].required = True
        self.fields['phonenumber'].required = True
        # self.fields['pro_card'].label = 'turlu'
        # self.fields['pro_card'].choices = ((1, "Oui"), (0, "Non"))
        # self.fields['pro_card'].label = 'turlu'
        # self.fields['pro_card'].widget = 'forms.RadioSelect'
        # self.fields['pro_card'].initial = '0'
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7'
        self.helper.form_method = 'post'
        self.helper.action = reverse('agent:update')
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Accordion(
                AccordionGroup(
                    '1) Coordonnees',
                    'address1',
                    'address2',
                    'zipcode',
                    'city',
                    'phonenumber',
                ),
                AccordionGroup('2) Naissance',
                    'birthdate',
                    'birthplace'),
                AccordionGroup('3) Papiers identite',
                    'id_card_type',
                    'id_card_validity_start_date',
                    'id_card_validity_end_date',
                    ),
                AccordionGroup('4) Carte vitale',
                    'vital_card_validity_start_date',
                    'vital_card_validity_end_date',
                    ),
                AccordionGroup('4) Carte professionnelle',
                    'pro_card',
                    'pro_card_validity_start_date',
                    'pro_card_validity_end_date',
                    ),
            )
        )
        self.helper.layout.append(Submit('save', 'Valider'))

    class Meta:
        # Set this form to use the User model.
        model = Agent

        # exclude = ('user', 'pole_emploi_start_date', 'pole_emploi_end_date', 'certifications')
        exclude = ('user', 'pole_emploi_start_date', 'pole_emploi_end_date','certifications')
        widgets = {
            #Use localization and bootstrap 3
            'birthdate': DateWidget(usel10n = True, bootstrap_version=3),
            'id_card_validity_start_date': DateWidget(usel10n = True, bootstrap_version=3),
            'id_card_validity_end_date': DateWidget(usel10n = True, bootstrap_version=3),
            'vital_card_validity_start_date': DateWidget(usel10n = True, bootstrap_version=3),
            'vital_card_validity_end_date': DateWidget(usel10n = True, bootstrap_version=3),
            'pro_card_validity_start_date': DateWidget(usel10n = True, bootstrap_version=3),
            'pro_card_validity_end_date': DateWidget(usel10n = True, bootstrap_version=3),
        }


class PoleEmploiForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = Agent

        # Constrain the UserForm to just these fields.
        fields = ("pole_emploi_start_date", "pole_emploi_end_date")

        exclude = ('address1',)

        pole_emploi = forms.BooleanField(
                label ="Etes-vous isncrits a Pole emploi",
                required =True,
            )

class CertificationsFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(CertificationsFormHelper, self).__init__(*args, **kwargs)
        self.form_class = 'form-horizontal'
        self.label_class = 'col-lg-5'
        self.field_class = 'col-lg-5'
        self.form_method = 'post'
        self.template = 'bootstrap/table_inline_formset.html'
        self.action = reverse('agent:update')
        self.add_input(Submit('save', 'Valider'))



class AgentCertificationsForm(forms.ModelForm):
    model = AgentCertification

    #def __init__(self, *args, **kwargs):
        #super(AgentCertificationsForm, self).__init__(*args, **kwargs)
        #self.fields['start_date'].widget = DateWidget(usel10n = True, bootstrap_version=3)
    class Meta:
        model = AgentCertification
        # Set this form to use the User model.
        # model = Agent

        # exclude = ('user', 'pole_emploi_start_date', 'pole_emploi_end_date', 'certifications')
        widgets = {
            'start_date': DateWidget(usel10n = True, bootstrap_version=3),
        }
