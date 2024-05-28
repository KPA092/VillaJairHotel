from django.contrib import admin
from . models import States

@admin.register(States)
class StatesAdmin(admin.ModelAdmin):
    list_display = ('id_state', 'state_name', 'id_type_state') #listar todos los campos de la tabla
   # search_fields = ('state_name', 'id_type_state') #buscador
    #list_per_page = 2




