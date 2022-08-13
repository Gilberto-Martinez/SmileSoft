from django.urls import path
from .views import *
from .forms import *

from gestion_tratamiento.views import PacienteList2
urlpatterns = [
            path('listar_insumo/', listar_insumo, name="listar_tratamiento"),
            path('eliminar_insumo/<nombre_insumo>/', eliminar_insumo, name="eliminar_insumo"),
            path('agregar_insumo/', agregar_insumo, name="agregar_insumo"),
            path('modificar_insumos/<nombre_insumo>/', modificar_insumo, name="modificar_insumos"),          
            path('listar_paciente2/', PacienteList2.as_view(),  name="listar_paciente2"),
]