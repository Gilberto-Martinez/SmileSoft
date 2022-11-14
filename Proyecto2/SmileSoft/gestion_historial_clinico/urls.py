from django.urls import path
from .views import *

urlpatterns = [
    path('listar_pacientes_historial/', listar_pacientes_historial, name="listar_pacientes_historial"),
    path('listar_historial_clinico/<int:id_paciente>', listar_historial_clinico, name="listar_historial_clinico"),
    path('ver_mi_historial_clinico/<numero_documento>', ver_mi_historial_clinico, name="ver_mi_historial_clinico"),
    # path('permiso_mensaje/<str:titulo>/<str:mensaje>', permiso_mensaje, name="permiso_mensaje"),
]