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
