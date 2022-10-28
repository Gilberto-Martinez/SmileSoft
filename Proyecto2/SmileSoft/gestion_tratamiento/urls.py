from django.urls import path
from .views import *
from .forms import *

urlpatterns = [
            path('listar_tratamiento/', listar_tratamiento, name="listar_tratamiento"),
            path('listar_tratamiento_categoria/', TratamientoCategoriaList.as_view(), name="listar_tratamiento_categoria"),
            path('eliminar_tratamiento/<codigo_tratamiento>/', eliminar_tratamiento, name="eliminar_tratamiento"),
            path('agregar_tratamiento/', agregar_tratamiento, name="agregar_tratamiento"),
            path('modificar_tratamiento/<int:codigo_tratamiento>/', modificar_tratamiento, name="modificar_tratamiento"),          
            path('listar_paciente2/', PacienteList2.as_view(),  name="listar_paciente2"),
            path('asignar_tratamientos/<int:id_paciente>', asignar_tratamientos, name="asignar_tratamientos"),
            path('tratamientos_asignados/<int:pk>', DetalleTratamientosAsignados.as_view(), name="tratamientos_asignados"),
            path('listar_tratamientos_asignados/<int:id_paciente>', listar_tratamiento_asignado, name="listar_tratamientos_asignados"),
            path('eliminar_tratamiento_asignado/<id_pac_tratamiento>/<cedula>', eliminar_tratamiento_asignado, name="eliminar_tratamiento_asignado"),
            #path('agregar_insumo_asignado/<int:pk>', InsumoAsignado.as_view(), name="agregar_insumo_asignado"),
            # path('listar_insumos_asignados/<cod_tratamiento>', listar_insumos_asignado, name="listar_insumos_asignado"),
            path('listar_tratamientos_pendientes/', listar_tratamientos_pendientes, name="listar_tratamientos_pendientes"),
            path('realizar_pregunta/<str:id_tratamiento_conf>', preguntar_confirmacion, name="realizar_pregunta"),
            path('confirmar_tratamientos/<str:id_tratamiento_conf>', confirmar_tratamiento, name="confirmar_tratamientos"),
            path('mostrar_mensaje_confirmacion/<str:id_tratamiento_conf>', mostrar_mensaje_confirmacion, name="mostrar_mensaje_confirmacion"),
            # path('tratamiento_asignado_exitoso/', mostrar_mensaje_confirmacion, name="mostrar_mensaje_confirmacion/"),
            path('ver_mis_tratamientos_pendientes/<numero_documento>', ver_mis_tratamientos_pendientes, name="ver_mis_tratamientos_pendientes"),
]