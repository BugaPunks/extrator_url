"""
URLs de la aplicacion extractor
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('extraer', views.extraer, name='extraer'),
    path('exportar', views.exportar, name='exportar'),
]
