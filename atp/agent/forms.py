# -*- coding: utf-8 -*-
from django import forms
from .models import Agent
from .models import AgentCertification
from .models import AgentIdCard
from .models import AgentAddress
from .models import AgentProCard
from .models import AgentQualification
from .models import AgentVarious
from datetimewidget.widgets import DateWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Submit
from django.core.urlresolvers import reverse
from ajax_upload.widgets import AjaxClearableFileInput


class AgentIdCardForm(forms.ModelForm):

    class Meta:
        model = AgentIdCard
        exclude = ('agent',)
        widgets = {
            'id_card_front': AjaxClearableFileInput,
            'id_card_back': AjaxClearableFileInput,
            'id_card_validity_start_date': DateWidget(usel10n=True, bootstrap_version=3),
            'id_card_validity_end_date': DateWidget(usel10n=True, bootstrap_version=3),
        }

    def __init__(self, *args, **kwargs):
        super(AgentIdCardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['id_card_validity_end_date'].required = True
        self.fields['id_card_validity_start_date'].required = True
        self.fields['id_card_type'].required = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('agent:~agent_id_card')
        self.helper.layout = Layout(
            Fieldset(
                u'1) Sélectionnez le type de papier et renseignez les dates de début et de fin de validité',
                'id_card_type',
                'id_card_validity_start_date',
                'id_card_validity_end_date',
            ),
            Fieldset(
                u'2) Télécharger le verso et le recto de votre document.',
                'id_card_front',
                'id_card_back'
            ),
        )
        self.helper.layout.append(Submit('save', 'Valider'))


class AgentForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = Agent

        exclude = ('user', 'pole_emploi_start_date', 'pole_emploi_end_date', 'certifications', 'form_state', 'qualifications', 'vital_card_vitality_start_date', 'vital_card_vitality_end_date')
        widgets = {
            'birthdate': DateWidget(usel10n=True, bootstrap_version=3),
            'vital_card_validity_start_date': DateWidget(usel10n=True, bootstrap_version=3),
            'vital_card_validity_end_date': DateWidget(usel10n=True, bootstrap_version=3),
            'pro_card_validity_start_date': DateWidget(usel10n=True, bootstrap_version=3),
            'pro_card_validity_end_date': DateWidget(usel10n=True, bootstrap_version=3),
            'picture': AjaxClearableFileInput
        }

    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        self.fields['genre'].required = True
        self.fields['firstname'].required = True
        self.fields['lastname'].required = True
        self.fields['birthdate'].required = True
        self.fields['birthplace'].required = True
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form = 'AGENT'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('agent:~agent')
        self.helper.layout = Layout(
            Fieldset(u'1) Indiquez votre genre, votre nom et votre prénom',
                     'genre', 'firstname', 'lastname'),
            Fieldset('2) Indiquez votre date de naissance puis votre lieu de naissance',
                     'birthdate',
                     'birthplace'),
            Fieldset('4) Photo identite',
                     'picture',),
        )
        self.helper.layout.append(Submit('save', 'Valider'))


class AgentAddressForm(forms.ModelForm):

    class Meta:
        model = AgentAddress
        exclude = ('agent',)

    def __init__(self, *args, **kwargs):
        super(AgentAddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['address1'].required = True
        self.fields['zipcode'].required = True
        self.fields['city'].required = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('agent:~agent_address')
        self.helper.layout = Layout(
            Fieldset('1) Adresse',
                     'address1',
                     'address2',
                     'zipcode',
                     'city',),
            Fieldset(u'2) Téléphone',
                     'mobilephonenumber',
                     'fixephonenumber',),
        )
        self.helper.layout.append(Submit('save', 'Valider'))


class AgentProCardForm(forms.ModelForm):

    class Meta:
        model = AgentProCard
        exclude = ('agent',)
        widgets = {
            'pro_card_validity_start_date': DateWidget(usel10n=True, bootstrap_version=3),
            'pro_card_validity_end_date': DateWidget(usel10n=True, bootstrap_version=3),
            'pro_card_front': AjaxClearableFileInput,
            'pro_card': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super(AgentProCardForm, self).__init__(*args, **kwargs)
        self.fields['pro_card'].required = True
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-3'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('agent:~agent_pro_card')
        self.helper.layout = Layout(
            Fieldset(u'Precisez si vous etes titulaire de la carte professionnelle',
                     'pro_card',
                     'pro_card_validity_start_date',
                     'pro_card_validity_end_date',
                     'pro_card_front',
                     ),
        )
        self.helper.layout.append(Submit('save', 'Valider'))


class AgentQualificationsFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(AgentQualificationsFormHelper, self).__init__(*args, **kwargs)
        self.template = 'agent/crispy/table_inline_formset.html'
        self.add_input(Submit('save', 'Valider'))


class AgentQualificationsForm(forms.ModelForm):

    class Meta:
        model = AgentQualification

        widgets = {
            'qualification': forms.Select(attrs={'data-width': 'auto'}),
            'start_date': DateWidget(usel10n=True, bootstrap_version=3),
            'end_date': DateWidget(usel10n=True, bootstrap_version=3),
        }


class CertificationsFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(CertificationsFormHelper, self).__init__(*args, **kwargs)
        self.template = 'agent/crispy/table_inline_formset.html'
        self.add_input(Submit('save', 'Valider'))


class AgentCertificationsForm(forms.ModelForm):
    model = AgentCertification

    class Meta:
        model = AgentCertification

        widgets = {
            'certification': forms.Select(attrs={'data-width': 'auto'}),
            'start_date': DateWidget(usel10n=True, bootstrap_version=3),
            'end_date': DateWidget(usel10n=True, bootstrap_version=3),
            'picture': AjaxClearableFileInput
        }

        
class AgentVariousForm(forms.ModelForm):


    class Meta:
        model = AgentVarious
        exclude = ('agent',)
        widgets = {
            'car_license_start_date': DateWidget(usel10n=True, bootstrap_version=3),
            'car_license_end_date': DateWidget(usel10n=True, bootstrap_version=3),
        }

    def __init__(self, *args, **kwargs):
        super(AgentVariousForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['has_car'].required = True
        self.fields['has_car'].label = 'Possédez-vous une voiture ?'
        self.fields['has_motorbike'].required = True
        self.fields['has_motorbike'].label = 'Possédez-vous une moto, un scooter ?'
        self.fields['has_car_license'].required = True
        self.fields['has_car_license'].label = 'Possédez-vous un permis de conduire voiture valide ?'
        self.fields['car_license_type'].label = 'Indiquez le type de permis de conduire voiture ici'
        self.fields['car_license_start_date'].label = 'Indiquez la date de délivrance de votre permis de conduire voiture'
        self.fields['car_license_end_date'].label = 'Indiquez la date de fin de validité de votre permis de conduire voiture'
        self.fields['has_motorbike_license'].required = True
        self.fields['has_motorbike_license'].label = 'Possédez-vous un permis moto valide ?'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-7'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('agent:~agent_various')
        self.helper.layout = Layout(
            Fieldset(
                u'1) Possédez-vous une voiture, une moto, un scooter ? ',
                'has_car',
                'has_motorbike',
            ),
            Fieldset(
                u'2) Permis voiture',
                'has_car_license',
                'car_license_type',
                'car_license_start_date',
                'car_license_end_date'
            ),
            Fieldset(
                u'3) Permis moto',
                'has_motorbike_license',
            ),
        )
        self.helper.layout.append(Submit('save', 'Valider'))
