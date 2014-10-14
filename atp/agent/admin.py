from django.contrib import admin
from agent.models import *
from users.models import User

# Register your models here.


class AgentAdmin(admin.ModelAdmin):
    pass


class CertificationAdmin(admin.ModelAdmin):
    pass

#class CertificationInline(admin.TabularInline):
    #model = AgentCertification


admin.site.register(Agent,AgentAdmin)
# admin.site.register(Certification,CertificationAdmin)
