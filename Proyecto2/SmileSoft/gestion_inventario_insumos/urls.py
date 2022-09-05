from django.urls import path

# from gestion_tratamiento.views import asignar_insumos
from .views import *
from .forms import *

from gestion_tratamiento.views import PacienteList2
urlpatterns = [
            path('listar_insumo/', listar_insumo, name="listar_tratamiento"),
            path('eliminar_insumo/<nombre_insumo>/', eliminar_insumo, name="eliminar_insumo"),
            path('agregar_insumo/', agregar_insumo, name="agregar_insumo"),
            path('modificar_insumos/<nombre_insumo>/', modificar_insumo, name="modificar_insumos"),          
            path('listar_paciente2/', PacienteList2.as_view(),  name="listar_paciente2"),
            # path('asignar_insumos/<int:codigo_tratamiento>', asignar_insumos, name="asignar_insumos"),
            # path('tratamientos_asignados/<int:pk>', DetalleTratamientosAsignados.as_view(), name="tratamientos_asignados"),
            # path('listar_tratamientos_asignados/<int:id_paciente>', listar_tratamiento_asignado, name="listar_tratamientos_asignados"),
            # path('eliminar_tratamiento_asignado/<id_pac_tratamiento>/<cedula>', eliminar_tratamiento_asignado, name="eliminar_tratamiento_asignado"),
            # path('agregar_insumo_asignado/<int:pk>', InsumoAsignado.as_view(), name="agregar_insumo_asignado"),
            # # path('listar_insumos_asignados/<cod_tratamiento>', listar_insumos_asignado, name="listar_insumos_asignado"),
            # path('listar_tratamientos_pendientes/', listar_tratamientos_pendientes, name="listar_tratamientos_pendientes"),
            # path('realizar_pregunta/<str:id_tratamiento_conf>', preguntar_confirmacion, name="realizar_pregunta"),
            # path('confirmar_tratamientos/<str:id_tratamiento_conf>', confirmar_tratamiento, name="confirmar_tratamientos"),
            # path('mostrar_mensaje_confirmacion/<str:id_tratamiento_conf>', mostrar_mensaje_confirmacion, name="mostrar_mensaje_confirmacion/"),
            
]
