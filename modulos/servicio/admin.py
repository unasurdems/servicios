from datetime import datetime as dt
from django.contrib import admin

from agbc_servicio.admin import ModelLogAdmin

from .models import Servicio

@admin.register(Servicio)
class ServicioAdmin(ModelLogAdmin):
    list_display = (
        'nombre_facturacion',
        'ci_nit',
        'ciudad',
        'urbano_rural',
        'departamento',
        'provincia',
        'municipio',
        'zona',
        'marker'
    )
