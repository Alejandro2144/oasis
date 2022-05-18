"""Oasis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from backend import views as backendViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', backendViews.home),
    path('home/', backendViews.home),
    path('accounts/', include('django.contrib.auth.urls')),
    path('historias/', backendViews.tabla_historias),
    path('historias/buscar/', backendViews.buscar_historia),
    path('historias/crear/', backendViews.crear_historia),
    path('registro/', backendViews.registrar, name ='registro'),
    path('exportar/', backendViews.exportar_csv, name ='exportar'),
    path('historias/<int:ID>/', backendViews.ver_historia, name="historia_details"),
    path('informacion_investigador/', backendViews.ver_informacion_investigador, name="historia_details"),
    path('migraciones/', backendViews.migrar_informacion, name="migraciones")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
