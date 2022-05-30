from django.urls import path
from .views import *

urlpatterns = [
            path('listar_tratamiento/', listar_tratamiento, name="listar_tratamiento"),
            path('eliminar_tratamiento/<nombre_tratamiento>/', eliminar_tratamiento, name="eliminar_tratamiento"),
            path('agregar_tratamiento/', agregar_tratamiento, name="agregar_tratamiento"),
            path('modificar_tratamiento/<nombre_tratamiento>/', modificar_tratamiento, name="modificar_tratamiento"),
]