from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model

from modulos.parametro.models import LogModel

Usuario = get_user_model()

class Departamento(LogModel):
    departamento = models.CharField(_('Nombre del departamento'), max_length=15, null=False, blank=False, unique=True)
    departamento_descripcion = models.CharField(_('Descripcion del departamento'), max_length=50, null=True, blank=True)

    def __str__(self):
        return self.departamento


class Provincia(LogModel):
    provincia = models.CharField(_('Nombre de la provincia'), max_length=50, null=False, blank=False, unique=True)
    provincia_descripcion = models.CharField(_('Descripcion de la provincia'), max_length=80, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, related_name='departamento_provincia' , on_delete=models.PROTECT)

    def __str__(self):
        return self.provincia


class Alcaldia(LogModel):
    alcaldia = models.CharField(_('Nombre de la Alcaldia'), max_length=100, null=False, blank=False, unique=True)
    sigla = models.CharField(_('Sigla de la Alcaldia'), max_length=15, null=True, blank=True)
    dpa = models.CharField(_('DPA de la Alcaldia'), max_length=50, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % format(self.sigla, self.alcaldia)


class Municipio(LogModel):
    municipio = models.CharField(_('Nombre del municipio'), max_length=100, null=False, blank=False, unique=True)
    municipio_descripcion = models.CharField(_('Descripcion del municipio'), max_length=150, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, related_name='provincia_municipio', on_delete=models.PROTECT)
    alcaldia = models.ForeignKey(Alcaldia, related_name='alcaldia_municipio', on_delete=models.PROTECT)

    def __str__(self):
        return self.municipio


class Zona(LogModel):
    zonauv = models.CharField(_('Zona Unidad Vecinal'), max_length=150, null=True, blank=True)
    zonauv_codigo_zona_completo = models.CharField(_('Zona Codigo completo'), max_length=150, null=True, blank=True)
    zonauv_codigo_zona = models.CharField(_('Zona codigo'), max_length=150, null=True, blank=True)
    zonauv_descr = models.TextField(_('Zona UV descripcion'), null=True, blank=True)
    zonauv_cod_adm = models.CharField(_('Zona Codigo Adm'), max_length=150, null=True, blank=True)
    municipio = models.ForeignKey(Municipio, related_name='zona_municipio', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.zonauv


class Marker(LogModel):
    marker = models.CharField(_('Marker'), max_length=150, null=True, blank=True)
    marker_id = models.CharField(_('Marker ID'), max_length=15, null=True, blank=True)
    marker_position = models.CharField(_('Marker Posicion'), max_length=150, null=True, blank=True)
    marker_lat = models.CharField(_('Marker Latitud'), max_length=15, null=True, blank=True)
    marker_long = models.CharField(_('Marker Longitud'), max_length=15, null=True, blank=True)
    marker_visible = models.CharField(_('Marker Visible'), max_length=10, null=True, blank=True)
    marker_visible2 = models.CharField(_('Marker Visible 2'), max_length=10, null=True, blank=True)
    marker_drag = models.CharField(_('Marker Drag'), max_length=150, null=True, blank=True)
    zona = models.ForeignKey(Zona, related_name='marker_zona', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.marker


class Direccion(LogModel):
    zona_barrio_uv_otro = models.CharField(_('Zona Barrio UV Otro'), max_length=100, null=True, blank=True)
    calle_avenida = models.CharField(_('Calle/Avenida'), max_length=100, null=True, blank=True)
    dir_referencial = models.CharField(_('Dir. Referencial'), max_length=100, null=True, blank=True)
    numero = models.CharField(_('Numero'), max_length=50, null=True, blank=True)
    edificio = models.CharField(_('Edificio'), max_length=100, null=True, blank=True)
    piso = models.CharField(_('Piso'), max_length=50, null=True, blank=True)
    departamento_local_oficina = models.CharField(_('Departamento Local Oficina'), max_length=50, null=True, blank=True)
    longitud = models.CharField(_('Longitud'), max_length=15, null=True, blank=True)
    latitud = models.CharField(_('Latitud'), max_length=15, null=True, blank=True)
    servicio_id = models.IntegerField(_('Servicio ID'), null=False, blank=False, unique=True)

