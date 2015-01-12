from django.contrib import admin 
from clients.models import *

class SelectionAdmin(admin.ModelAdmin):
    pass

class ClientAdmin(admin.ModelAdmin):
    pass


class StatesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Selection, SelectionAdmin)
admin.site.register(States, StatesAdmin)
admin.site.register(Client, ClientAdmin)
