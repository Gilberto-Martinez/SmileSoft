from django.urls import path
from .views import *

urlpatterns = [
    path('listar_pacientes_historial/', listar_pacientes_historial, name="listar_pacientes_historial"),
    path('listar_historial_clinico/<int:id_paciente>', listar_historial_clinico, name="listar_historial_clinico"),
]