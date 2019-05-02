from datetime import datetime as dt
from django.contrib import admin

from agbc_servicio.admin import ModelLogAdmin

from .models import (
    Departamento,
    Provincia,
    Alcaldia,
    Municipio
)


@admin.register(Departamento)
class DepartamentoAdmin(ModelLogAdmin):
    list_display = (
        'departamento',
        'departamento_descripcion'
    )


@admin.register(Provincia)
class ProvinciaAdmin(ModelLogAdmin):
    list_display = (
        'provincia',
        'provincia_descripcion'
    )


@admin.register(Alcaldia)
class AlcaldiaAdmin(ModelLogAdmin):
    list_display = (
        'alcaldia',
        'sigla',
        'dpa'
    )


@admin.register(Municipio)
class MunicipioAdmin(ModelLogAdmin):
    list_display = (
        'municipio',
        'municipio_descripcion'
    )
