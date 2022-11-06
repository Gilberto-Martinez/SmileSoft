from django.urls import path

# from gestion_tratamiento.views import asignar_insumos
from .views import *
from .forms import *

from gestion_tratamiento.views import PacienteList2
urlpatterns = [
            path('listar_insumo/', listar_insumo, name="listar_tratamiento"),
            path('insumo_lista/', listar_insumo, name="insumo_lista"),
            path('eliminar_insumo/<codigo_insumo>/',eliminar_insumo, name="eliminar_insumo"),
            path('agregar_insumo/', agregar_insumo, name="agregar_insumo"),
            path('modificar_insumos/<codigo_insumo>/',modificar_insumo, name="modificar_insumos"),
            path('listar_paciente2/', PacienteList2.as_view(),  name="listar_paciente2"),
            path('asignar_insumos/<int:codigo_tratamiento>', asignar_insumos, name="asignar_insumos"),
            path('listar_insumos_asignados/<codigo_tratamiento>', listar_insumo_asignado, name="listar_insumos_asignados"),
            path('editar_cantidad_insumo_asignado/<id_tratamiento_insumo>', editar_cantidad_insumos_asig, name="editar_cantidad_insumo_asignado"),
            # path('insumo_asignado_exitoso/<codigo_tratamiento>',mostrar_insumo_asignado_exitoso,name="insumo_asignado_exitoso"),
            
            
            path('insumo_pdf/', ListaInsumoPDF.as_view(),name="insumo_pdf"),
            #path('insumo_lista/', listar_insumo_simple, name="insumo_lista"),
]
