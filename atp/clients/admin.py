from django.contrib import admin 
from clients.models import *

class SelectionAdmin(admin.ModelAdmin):
    pass

class CompanyAdmin(admin.ModelAdmin):
    pass

class StatesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Selection, SelectionAdmin)
admin.site.register(States, StatesAdmin)
admin.site.register(Company, CompanyAdmin)
