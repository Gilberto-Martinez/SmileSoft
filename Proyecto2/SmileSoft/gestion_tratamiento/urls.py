from django.urls import path
from .views import *
from .forms import *

urlpatterns = [
            path('listar_tratamiento/', listar_tratamiento, name="listar_tratamiento"),
            path('eliminar_tratamiento/<nombre_tratamiento>/', eliminar_tratamiento, name="eliminar_tratamiento"),
            path('agregar_tratamiento/', agregar_tratamiento, name="agregar_tratamiento"),
            path('modificar_tratamiento/<nombre_tratamiento>/', modificar_tratamiento, name="modificar_tratamiento"),          
            path('listar_paciente2/', PacienteList2.as_view(),  name="listar_paciente2"),
            path('asignar_tratamientos/<int:id_paciente>', asignar_tratamientos, name="asignar_tratamientos"),
            path('tratamientos_asignados/<int:pk>', DetalleTratamientosAsignados.as_view(), name="tratamientos_asignados"),
            path('listar_tratamientos_asignados/<int:id_paciente>', listar_tratamiento_asignado, name="listar_tratamientos_asignados"),
            path('eliminar_tratamiento_asignado/<id_pac_tratamiento>/<cedula>', eliminar_tratamiento_asignado, name="eliminar_tratamiento_asignado"),
            path('agregar_insumo_asignado/<int:pk>', InsumoAsignado.as_view(), name="agregar_insumo_asignado"),
            # path('listar_insumos_asignados/<cod_tratamiento>', listar_insumos_asignado, name="listar_insumos_asignado"),
            path('listar_tratamientos_pendientes/', listar_tratamientos_pendientes, name="listar_tratamientos_pendientes"),
            path('realizar_pregunta/<str:id_tratamiento_asig>', preguntar_confirmacion, name="realizar_pregunta"),
            path('confirmar_tratamientos/<str:id_tratamiento_asig>', confirmar_tratamiento, name="confirmar_tratamientos"),
]