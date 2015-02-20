# -*- coding: utf-8 -*-
from django import forms

from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Fieldset
from crispy_forms.layout import HTML 
from crispy_forms.layout import Submit
from django.core.urlresolvers import reverse


class UserForm(forms.ModelForm):
    # first_name = forms.CharField(max_length=30, label='Nom')

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = ("type", "first_name", "last_name")
        #widgets = {
            #'type': forms.RadioSelect,
        #}

    def __init__(self, *args, **kwargs):
        # print "SELF USR REQUEST : ", self.request
        # self.request = kwargs.pop("request")
        #print self.__dict__ 
        #initial = kwargs.get('initial', {})
        #print "INITIAL : ", initial
        #initial['type'] = 'CL'
        super(UserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['type'].label = u"Choisissez si vous êtes une entreprise (Client) ou un candidat (Agent)"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-12'
        self.helper.field_class = 'col-lg-3'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('users:update')
        #self.helper.layout = Layout(
            #Fieldset(u'Precisez votre nom et vos prenoms',
                     #'type',
        #)
            #)
        #self.helper.layout.append(
            #HTML(
                #'<button class="btn btn-primary btn-block" type="submit">dededede</button>'
            #)
        #)
        # self.helper.layout.append(Submit('save', 'Valider'))

    def signup(self, request, user):
        print "PASS DANS SIGNUP"
        user.save()


class UserFormUpdate(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(UserFormUpdate, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-12'
        self.helper.field_class = 'col-lg-3'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('users:update')

    def signup(self, request, user):
        print "PASS DANS SIGNUP"
        user.save()
