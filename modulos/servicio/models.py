from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model

from modulos.parametro.models import LogModel
from modulos.direccion.models import (
    Departamento,
    Provincia,
    Municipio,
    Zona,
    Marker
)

Usuario = get_user_model()

class Servicio(LogModel):
    nombre_facturacion = models.CharField(_('Nombre de Facturacion'), max_length=100, null=False, blank=False)
    ci_nit = models.CharField(_('CI/NIT'), max_length=15, null=False, blank=False)
    ciudad = models.CharField(_('Ciudad'), max_length=100, null=False, blank=False)
    urbano_rural = models.CharField(_('Urbano/Rural'), max_length=100, null=False, blank=False)
    departamento = models.ForeignKey(Departamento, related_name='servicio_departamento', on_delete=models.PROTECT, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, related_name='servicio_provincia', on_delete=models.PROTECT, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, related_name='servicio_municipio', on_delete=models.PROTECT, null=True, blank=True)
    zona = models.ForeignKey(Zona, related_name='servicio_zona', on_delete=models.PROTECT, null=True, blank=True)
    marker = models.ForeignKey(Marker, related_name='servicio_marker', on_delete=models.PROTECT, null=True, blank=True)