from django.contrib import admin
from agent.models import *
from users.models import User

# Register your models here.

class CertificationsInline(admin.StackedInline):
    model = AgentCertification
    suit_classes = 'suit-tab suit-tab-certifications'


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

    def has_delete_permission(self, request, obj=None):
            return False


class AgentProCardInline(admin.StackedInline):
    model = AgentProCard
    max_num = 1
    extra = 0
    suit_classes = 'suit-tab suit-tab-pro_card'

    def has_delete_permission(self, request, obj=None):
            return False


class AgentAdmin(admin.ModelAdmin):
    inlines = (CertificationsInline, AgentIdCardInline, AgentAddressInline, AgentProCardInline)

    fieldsets = [
            (None, {
                'classes': ('suit-tab', 'suit-tab-etat_civil'),
                'fields': ['genre', 'nationality', 'birthdate', 'birthplace']
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



class CertificationAdmin(admin.ModelAdmin):
    pass

#class CertificationInline(admin.TabularInline):
    #model = AgentCertification


admin.site.register(Agent,AgentAdmin)
# admin.site.register(Certification,CertificationAdmin)
