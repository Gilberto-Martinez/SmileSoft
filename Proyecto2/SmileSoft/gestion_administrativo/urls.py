from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [
          
            path('modificar_empresa/<ruc>/', modificar_empresa, name="modificar_empresa"),
    # path('datos_empresa/', datos_empresa, name="datos_empresa"),
            path('agregar_persona/', PersonaCreate.as_view(), name="agregar_persona"),
            path('agregar_persona_paciente/<str:pk>', PersonaPacienteCreate.as_view(),  name="agregar_persona_paciente"),
            path('agregar_paciente/', PacienteCreate.as_view(),  name="agregar_paciente"),
            path('agregar_funcionario/', FuncionarioCreate.as_view(),  name="agregar_funcionario"),
            path('agregar_especialista_salud/', EspecialistaSaludCreate.as_view(),  name="agregar_especialista_salud"),
            path('agregar_proveedor/', ProveedorCreate.as_view(),  name="agregar_proveedor"),
            path('agregar_cargo/', CargoCreate.as_view(),  name="agregar_cargo"),
            path('agregar_especialidad/', EspecialidadCreate.as_view(),  name="agregar_especialidad"),
            path('listar_persona/', PersonaList.as_view(),  name="listar_persona"),
            # path('listar_persona/', listar_persona,  name="listar_persona"),
            path('listar_funcionario/', FuncionarioList.as_view(),  name="listar_funcionario"),
            path('listar_paciente/', PacienteList.as_view(),  name="listar_paciente"),
            path('listar_especialista_salud/', EspecialistaSaludList.as_view(),  name="listar_especialista_salud"),
            path('listar_proveedor/', ProveedorList.as_view(),  name="listar_proveedor"),
            path('listar_cargo/', CargoList.as_view(),  name="listar_cargo"),
            path('listar_especialidad/', EspecialidadList.as_view(),  name="listar_especialidad"),
            path('editar_antecedente/<str:numero_documento>/',editar_antecedente, name="editar_antecedente"),
            path('editar_persona/<numero_documento>/', editar_persona, name="editar_persona"),
            path('modificar_persona/<str:pk>', PersonaUpdate.as_view(),  name="modificar_persona"),
            path('modificar_funcionario/<int:pk>', FuncionarioUpdate.as_view(),  name="modificar_funcionario"),
            path('modificar_especialista_salud/<int:pk>', EspecialistaSaludUpdate.as_view(),  name="modificar_especialista_salud"),
            path('modificar_paciente/<int:pk>', PacienteUpdate.as_view(),  name="modificar_paciente"),
            path('modificar_persona_paciente/<str:numero_documento>', modificar_persona_paciente,  name="modificar_persona_paciente"),
            # path('modificar_persona_paciente/<str:pk>', PersonaPacienteUpdate.as_view(),  name="modificar_persona_paciente"),
            path('modificar_proveedor/<str:pk>', ProveedorUpdate.as_view(),  name="modificar_proveedor"),
            path('modificar_cargo/<str:pk>', CargoUpdate.as_view(),  name="modificar_cargo"),
            path('modificar_especialidad/<int:pk>', EspecialidadUpdate.as_view(),  name="modificar_especialidad"),
            path('eliminar_persona/<str:pk>', PersonaDelete.as_view(),  name="eliminar_persona"),
            path('eliminar_funcionario/<int:pk>', FuncionarioDelete.as_view(),  name="eliminar_funcionario"),
            path('eliminar_especialista_salud/<int:pk>', EspecialistaSaludDelete.as_view(),  name="eliminar_especialista_salud"),
            path('eliminar_paciente/<int:pk>', PacienteDelete.as_view(),  name="eliminar_paciente"),
            path('eliminar_proveedor/<str:pk>', ProveedorDelete.as_view(),  name="eliminar_proveedor"),
            path('eliminar_cargo/<str:pk>', CargoDelete.as_view(),  name="eliminar_cargo"),
            path('eliminar_especialidad/<int:pk>', EspecialidadDelete.as_view(),  name="eliminar_especialidad"),
            path('correcto', SuccessView.as_view(),  name="correcto"),
            path('mensaje_error/', SuccessError.as_view(),  name="mensaje_error"),
            # path('asignar_tratamiento/<int:pk>', TratamientoAsignadoCreate.as_view(), name="asignar_tratamiento"),
            # path('modificar_tratamiento_asignado/<int:pk>', TratamientoAsignadoUpdate.as_view(), name="modificar_tratamiento_asignado"),
]