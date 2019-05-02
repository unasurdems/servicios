from django.db import models


class LogModel(models.Model):
    usuario_creacion = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificacion = models.IntegerField(null=True, blank=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)
    usuario_eliminacion = models.IntegerField(null=True, blank=True)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True