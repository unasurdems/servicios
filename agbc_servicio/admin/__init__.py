from datetime import datetime as dt
from django.contrib import admin


class ModelLogAdmin(admin.ModelAdmin):
    exclude = ('usuario_creacion', 'usuario_modificacion', 'usuario_eliminacion', 'fecha_modificacion', 'fecha_eliminacion')

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.filter(fecha_eliminacion__isnull=True)

    def save_model(self, request, obj, form, change):
        if change:
            obj.usuario_modificacion = request.user.id
            obj.fecha_modificacion = dt.now()
        else:
            obj.usuario_creacion = request.user.id
            obj.fecha_creacion = dt.now()
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        obj.usuario_eliminacion = request.user.id
        obj.fecha_eliminacion = dt.now()
        obj.save()