from django.urls import path

from .views import *


urlpatterns = [
    path("calendar/", Calendario.as_view(), name="calendario"),
    path('gracias/', calendario_vista, name="gracias"),
    path("calendario_usuario/", CalendarioUsuario.as_view(),name="calendario_usuario"),
    path('calendario_mensaje/', calendario_mensaje, name="calendario_mensaje"),

    # path('calendario_usuario/', calendario_usuario, name="calendario_usuario"),
    # path('calendar/', pruebacalendar, name="calendar"),

    # <---A Nivel Sistema-->
    path('listado_citas/', listar_cita, name="listado_citas"),
    path('agregar_cita/<int:id_paciente>', agregar_cita, name="agregar_cita"),
    
    path('agendar_cita/<int:id_paciente>/<int:codigo_tratamiento>', agendar_cita, name="agendar_cita"),
    path('agregar_cita_usuario/<int:id_paciente>/',addcita_cita_usuario, name="agregar_cita_usuario"),
    path('modificar_cita/<int:id_cita>', modificar_cita, name="modificar_cita"),
    path('modificar_cita_usuario/<int:id_cita>', modificar_cita_usuario, name="modificar_cita_usuario"),
    path('eliminar_cita/<int:id_cita>', eliminar_cita, name="eliminar_cita"),
    path('pacientes_cita/', listar_citapaciente, name="pacientes_cita"),

    path('cita_vista/<int:id_cita>/',cita_vista, name="cita_vista"),
    
    # <--- A NIVEL Usuario--> Con acceso al sistema
    path('usuario_addCita/<str:numero_documento>/', addcita_usuario, name="usuario_addCita"),
    path('usuario_changeCita/<int:id_cita>/',cambiarCita_usuario, name="usuario_addCita"),
    path('delete_cita/<int:id_cita>', deletecita, name='delete_cita'),
    
    #<-- Templates de mensajes
    path('horario_reservado/', horario_reservado, name='horario_reservado'),
    path('horario_duplicado/', horario_duplicado, name='horario_duplicado'),

    # <--Horarios-->
    path('agregar_hora/', agregar_hora, name="agregar_hora"),
    path('eliminar_hora/<int:id_hora>', eliminar_hora, name='eliminar_hora'),
    path('listar_hora/', listar_hora, name="listar_hora"),


]
