"""agbc_servicio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from modulos.seguridad import urls as urls_seguridad
from modulos.servicio import urls as urls_servicio
# from modulos.direccion import urls as urls_direccion
# from modulos.personal import urls as urls_personal


urlpatterns = [
    path('admin/', admin.site.urls),
    path('seguridad/', include(urls_seguridad)),
    path('servicio/', include(urls_servicio)),
    # path('direccion/', include(urls_direccion)),
    # path('personal/', include(urls_personal)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
