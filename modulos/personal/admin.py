from datetime import datetime as dt
from django.contrib import admin

from agbc_servicio.admin import ModelLogAdmin

from .models import(
    Oficina,
    Cargo,
    Profesion,
    TipoDocumento,
    Personal
)


@admin.register(Oficina)
class OficinaAdmin(ModelLogAdmin):
    list_display = ('oficina',)


@admin.register(Cargo)
class CargoAdmin(ModelLogAdmin):
    list_display = ('cargo',)


@admin.register(Profesion)
class ProfesionAdmin(ModelLogAdmin):
    list_display = ('profesion',)


@admin.register(TipoDocumento)
class TipoDocumentoAdmin(ModelLogAdmin):
    list_display = ('tipodocumento',)


@admin.register(Personal)
class PersonalAdmin(ModelLogAdmin):
    list_display = (
        'carnet',
        'tipodocumento',
        'nombre',
        'apellido_paterno',
        'apellido_materno',
        'genero',
        'profesion',
        'cargo',
        'oficina'
    )