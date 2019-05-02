from django.contrib import admin

from .models import Usuario, Menu, UsuarioMenu

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    exclude = ('password', 'last_login')
    search_fields = ('username', 'email', 'persona_id')
    list_display = ('persona_id', 'email', 'username', 'is_active')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(UsuarioMenu)
class UsuarioMenuAdmin(admin.ModelAdmin):
    pass