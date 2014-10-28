# -*- coding: utf-8 -*-
from django import forms

from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Submit
from django.core.urlresolvers import reverse


class UserForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-3'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('users:update')
        self.helper.layout = Layout(
            Fieldset(u'Precisez votre nom et vos prénoms',
                     'first_name',
                     'last_name',
                     ),
        )
        self.helper.layout.append(Submit('save', 'Valider'))
