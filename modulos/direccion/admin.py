from datetime import datetime as dt
from django.contrib import admin

from agbc_servicio.admin import ModelLogAdmin

from .models import (
    Departamento,
    Provincia,
    Alcaldia,
    Municipio,
    Zona,
    Marker,
    Direccion
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


@admin.register(Zona)
class ZonaAdmin(ModelLogAdmin):
    list_display = (
        'zonauv',
        'zonauv_codigo_zona_completo',
        'zonauv_codigo_zona',
        'zonauv_descr',
        'zonauv_cod_adm',
        'municipio'
    )


@admin.register(Marker)
class MarkerAdmin(ModelLogAdmin):
    list_display = (
        'marker',
        'marker_id',
        'marker_position',
        'marker_lat',
        'marker_long',
        'marker_visible',
        'marker_visible2',
        'marker_drag',
        'zona'
    )


@admin.register(Direccion)
class DireccionAdmin(ModelLogAdmin):
    list_display = (
        'zona_barrio_uv_otro',
        'calle_avenida',
        'dir_referencial',
        'numero',
        'edificio',
        'piso',
        'departamento_local_oficina',
        'longitud',
        'latitud',
        'servicio_id'
    )