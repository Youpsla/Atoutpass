# -*- coding: utf-8 -*-
from django import forms
from .models import Selection
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Submit


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
