from django.urls import path
from .views import *
from .views import *
from gestion_administrativo import *
from .forms import *

from gestion_administrativo.views import PacienteList2
from gestion_administrativo.views import *
urlpatterns = [
            path('listar_tratamiento/', listar_tratamiento, name="listar_tratamiento"),
            path('eliminar_tratamiento/<nombre_tratamiento>/', eliminar_tratamiento, name="eliminar_tratamiento"),
            path('agregar_tratamiento/', agregar_tratamiento, name="agregar_tratamiento"),
            path('modificar_tratamiento/<nombre_tratamiento>/', modificar_tratamiento, name="modificar_tratamiento"),          
            path('listar_paciente2/', PacienteList2.as_view(),  name="listar_paciente2"),
            # path('asignar_tratamiento/', asignar_tratamiento, name="asignar_tratamiento"),
            path('tratamientos_asignados/<int:pk>', DetalleTratamientosAsignados.as_view(), name="tratamientos_asignados"),
            path('listar_tratamientos_asignados/<cedula>', listar_tratamiento_asignado, name="listar_tratamientos_asignados"),
            path('eliminar_tratamiento_asignado/<id_pac_tratamiento>/<cedula>', eliminar_tratamiento_asignado, name="eliminar_tratamiento_asignado"),
            

]