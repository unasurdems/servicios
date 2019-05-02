from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model

from modulos.parametro.models import LogModel

Usuario = get_user_model()

class Oficina(LogModel):
    oficina = models.CharField(_('Nombre de la Oficina'), max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.oficina


class Cargo(LogModel):
    cargo = models.CharField(_('Nombre del Cargo'), max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.cargo


class Profesion(LogModel):
    profesion = models.CharField(_('Profesion'), max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.profesion

class TipoDocumento(LogModel):
    tipodocumento = models.CharField(_('Tipo de documento'), max_length=20, null=False, blank=False, unique=True)

    def __str__(self):
        return self.tipodocumento

class Personal(LogModel):
    carnet = models.CharField(_('Nro. CI'), max_length=10, null=False, blank=False, unique=True)
    tipodocumento = models.ForeignKey(TipoDocumento, related_name='personal_tipodocumento', on_delete=models.PROTECT)
    nombre = models.CharField(_('Nombre de la persona'), max_length=50, null=False, blank=False)
    apellido_paterno = models.CharField(_('Ap. paterno de la persona'), max_length=50, null=True, blank=True)
    apellido_materno = models.CharField(_('Ap. materno de la persona'), max_length=50, null=True, blank=True)
    nacionalidad = models.CharField(_('Nacionalidad'), max_length=10, null=True, blank=True)
    genero = models.CharField(_('Genero'), max_length=10, null=False, blank=False)
    fecha_nacimiento = models.DateField(_('Fecha de Nacimiento'), null=True, blank=True)
    profesion = models.ForeignKey(Profesion, related_name='personal_profesion', on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargo, related_name='personal_cargo', on_delete=models.PROTECT)
    oficina = models.ForeignKey(Oficina, related_name='personal_oficina', on_delete=models.PROTECT)

    def __str__(self):
        return '%s - %s %s %s' % format(self.carnet, self.apellido_paterno, self.apellido_materno, self.nombre)

