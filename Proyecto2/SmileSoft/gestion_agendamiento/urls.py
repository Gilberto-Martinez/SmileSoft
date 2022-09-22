from django.urls import path

from .views import *


urlpatterns = [

    path("calendar/", Calendario.as_view(), name="calendario"),
    path('gracias/', calendario_vista, name="gracias"),
    path("calendario_usuario/", CalendarioUsuario.as_view(),
         name="calendario_usuario"),
    # path('calendario_usuario/', calendario_usuario, name="calendario_usuario"),
    # path('calendar/', pruebacalendar, name="calendar"),

    # <--- A Sistema-->
    path('listado_citas/', listar_cita, name="listado_citas"),
    # path("listado_citas/", listaReserva.as_view(),
    #      name="listado_citas"),
    path('agregar_cita/<int:id_paciente>', agregar_cita, name="agregar_cita"),
    path('modificar_cita/<int:id_cita>', modificar_cita, name="modificar_cita"),
    path('eliminar_cita/<int:id_cita>', eliminar_cita, name="eliminar_cita"),
    path('pacientes_cita/', listar_citapaciente, name="pacientes_cita"),


    path('cita_vista/<int:id_cita>/',cita_vista, name="cita_vista"),
    
    # <--- A NIVEL USUARIO-->
    path('usuario_addCita/<str:numero_documento>/', addcita_usuario, name="usuario_addCita"),
    path('usuario_changeCita/<int:id_cita>/',cambiarCita_usuario, name="usuario_addCita"),
    path('delete_cita/<int:id_cita>', deletecita, name='delete_cita'),
    path('horario_reservado/', horario_reservado, name='horario_reservado'),
    path('horario_duplicado/', horario_duplicado, name='horario_duplicado'),

   
    path('calendario_mensaje/', calendario_mensaje, name="calendario_mensaje"),

    # <--Horarios-->
    path('agregar_hora/', agregar_hora, name="agregar_hora"),
    path('eliminar_hora/<int:id_hora>', eliminar_hora, name='eliminar_hora'),
    path('listar_hora/', listar_hora, name="listar_hora"),


]
