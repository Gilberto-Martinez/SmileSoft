from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [
            path('agregar_persona/', PersonaCreate.as_view(), name="agregar_persona"),
            path('agregar_paciente/', PacienteCreate.as_view(),  name="agregar_paciente"),
            path('agregar_funcionario/', FuncionarioCreate.as_view(),  name="agregar_funcionario"),
            path('agregar_especialista_salud/', EspecialistaSaludCreate.as_view(),  name="agregar_especialista_salud"),
            path('agregar_proveedor/', ProveedorCreate.as_view(),  name="agregar_proveedor"),
            path('agregar_cargo/', CargoCreate.as_view(),  name="agregar_cargo"),
            path('listar_persona/', PersonaList.as_view(),  name="listar_persona"),
            path('listar_funcionario/', FuncionarioList.as_view(),  name="listar_funcionario"),
            path('listar_paciente/', PacienteList.as_view(),  name="listar_paciente"),
            path('listar_especialista_salud/', EspecialistaSaludList.as_view(),  name="listar_especialista_salud"),
            path('listar_proveedor/', ProveedorList.as_view(),  name="listar_proveedor"),
            path('listar_cargo/', CargoList.as_view(),  name="listar_cargo"),
            path('modificar_persona/<str:pk>', PersonaUpdate.as_view(),  name="modificar_persona"),
            path('modificar_funcionario/<int:pk>', FuncionarioUpdate.as_view(),  name="modificar_funcionario"),
            path('modificar_especialista_salud/<int:pk>', EspecialistaSaludUpdate.as_view(),  name="modificar_especialista_salud"),
            path('modificar_paciente/<int:pk>', PacienteUpdate.as_view(),  name="modificar_paciente"),
            path('modificar_proveedor/<str:pk>', ProveedorUpdate.as_view(),  name="modificar_proveedor"),
            path('modificar_cargo/<str:pk>', CargoUpdate.as_view(),  name="modificar_cargo"),
            path('eliminar_persona/<str:pk>', PersonaDelete.as_view(),  name="eliminar_persona"),
            path('eliminar_funcionario/<int:pk>', FuncionarioDelete.as_view(),  name="eliminar_funcionario"),
            path('eliminar_especialista_salud/<int:pk>', EspecialistaSaludDelete.as_view(),  name="eliminar_especialista_salud"),
            path('eliminar_paciente/<int:pk>', PacienteDelete.as_view(),  name="eliminar_paciente"),
            path('eliminar_proveedor/<str:pk>', ProveedorDelete.as_view(),  name="eliminar_proveedor"),
            path('eliminar_cargo/<str:pk>', CargoDelete.as_view(),  name="eliminar_cargo"),
            path('correcto', SuccessView.as_view(),  name="correcto"),
            path('mensaje_error/', SuccessError.as_view(),  name="mensaje_error"),
]