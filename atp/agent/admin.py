from django.contrib import admin
from agent.models import *
from agent.forms import *
from django import forms
from ajax_upload.widgets import AjaxClearableFileInput
from suit.widgets import SuitDateWidget
from config.common import Common

# Register your models here.
from users.models import User


class AgentIdCardInlineForm(forms.ModelForm):
    class Meta:
        model = AgentIdCard
        widgets = {
                'id_card_front': AjaxClearableFileInput(),
                'id_card_back': AjaxClearableFileInput(),
                'id_card_validity_start_date': SuitDateWidget,
                'id_card_validity_end_date': SuitDateWidget,
                }


class AgentProCardInlineForm(forms.ModelForm):
    class Meta:
        model = AgentProCard
        widgets = {
                'pro_card_front': AjaxClearableFileInput(),
                }


class AgentCertificationInlineForm(forms.ModelForm):
    class Meta:
        model = AgentCertification
        widgets = {
                'picture': AjaxClearableFileInput(),
                }


class CertificationsInline(admin.StackedInline):
    model = AgentCertification
    suit_classes = 'suit-tab suit-tab-certifications'
    max_num = 3 
    extra =1 


class AgentAddressInline(admin.StackedInline):
    model = AgentAddress
    max_num = 1
    extra = 0
    suit_classes = 'suit-tab suit-tab-address'

    def has_delete_permission(self, request, obj=None):
            return False


class AgentIdCardInline(admin.StackedInline):
    model = AgentIdCard
    max_num = 1
    extra = 0
    suit_classes = 'suit-tab suit-tab-id_card'
    form = AgentIdCardInlineForm

    def has_delete_permission(self, request, obj=None):
            return False


class AgentProCardInline(admin.StackedInline):
    model = AgentProCard
    max_num = 1
    extra = 0
    suit_classes = 'suit-tab suit-tab-pro_card'
    form = AgentProCardInlineForm

    def has_delete_permission(self, request, obj=None):
            return False


class AgentAdminForm(forms.ModelForm):
    class Meta:
        model = Agent
        widgets = {
                'picture': AjaxClearableFileInput(),
                }

        
class AgentAdmin(admin.ModelAdmin):
    inlines = (CertificationsInline, AgentIdCardInline, AgentAddressInline, AgentProCardInline)
    form = AgentAdminForm

    fieldsets =[
            #('Compte', {
                #'classes': ('suit-tab', 'suit-tab-user'),
                #'fields': ['user', 'first_name']
                #}),
            ('Etat Civil', {
                'classes': ('suit-tab', 'suit-tab-etat_civil'),
                'fields': ['firstname', 'lastname', 'genre', 'nationality', 'birthdate', 'birthplace', 'picture']
                }),
            ('Papiers identite', {
                'classes': ('suit-tab', 'suit-tab-id_card'),
                'fields': ['user']
                }),
            ('Adresse', {
                'classes': ('suit-tab', 'suit-tab-address'),
                'fields': ['birthplace']
                }),
            ('Carte Pro', {
                'classes': ('suit-tab', 'suit-tab-pro_card'),
                'fields': ['user']
                }),
            ]
    suit_form_tabs = (('etat_civil', 'Etat civil'), ('id_card', 'Papiers identite'), ('address', 'Coordonnees'), ('pro_card', 'Carte Pro'), ('certifications', 'Certifications'))


    class Media:
        css ={ 
                'all':('ajax_upload/css/ajax-upload-widget.css',)
                }
        js =[ 
                'ajax_upload/js/ajax-upload-widget.js',
                'ajax_upload/js/jquery.iframe-transport.js',
                'js/project.js',
               ]


class CertificationAdmin(admin.ModelAdmin):
    pass



admin.site.register(Agent,AgentAdmin)
# admin.site.register(Certification,CertificationAdmin)
