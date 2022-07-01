from django.urls import path

from .views import *


urlpatterns = [
    
    path("calendar/", Calendario.as_view(), name="calendario"),
    # path('calendario/', calendario_vista, name="calendario"),
    # path('calendar/', pruebacalendar, name="calendar"),
    path('listado_citas/', listar_cita, name="listado_citas"),
    path('agregar_cita/', agregar_cita, name="agregar_cita"),
    path('modificar_cita/<cedula>',
         modificar_cita, name="modificar_cita"),
    path('eliminar_cita/<cedula>',
         eliminar_cita, name="eliminar_cita"),
]
