from django.urls import path

from .views import *


urlpatterns = [

    path("calendar/", Calendario.as_view(), name="calendario"),
    path('gracias/', calendario_vista, name="gracias"),
    path("calendario_usuario/", CalendarioUsuario.as_view(), name="calendario_usuario"),
    # path('calendario_usuario/', calendario_usuario, name="calendario_usuario"),
    # path('calendar/', pruebacalendar, name="calendar"),
    path('listado_citas/', listar_cita, name="listado_citas"),
    path('agregar_cita/<int:id_paciente>', agregar_cita, name="agregar_cita"),
    path('modificar_cita/<int:id_cita>', modificar_cita, name="modificar_cita"),
    path('eliminar_cita/<int:id_cita>', eliminar_cita, name="eliminar_cita"),
    path('pacientes_cita/', listar_citapaciente, name="pacientes_cita"),
  
    # A nivel usuario
     path('cita_vista/<int:id_cita>/',
         cita_vista, name="cita_vista"),
       
    path('usuario_addCita/<str:numero_documento>/',
         addcita_usuario, name="usuario_addCita"),
#     path('usuario_changeCita/<str:numero_documento>/',
#          cambiarCita_usuario, name="usuario_addCita"),
    path('usuario_changeCita/<int:id_cita>/',
         cambiarCita_usuario, name="usuario_addCita"),
    
    # path('eliminar_cita/<int:pk>',
    #      CitaDelete.as_view(),  name="eliminar_paciente"),
    path('delete_cita/<int:id_cita>', deletecita, name='delete_cita'),
    
    path('mis_citas/<numero_documento>', mis_citas_lista, name="mis_citas"),
    
    path('calendario_mensaje/', calendario_mensaje, name="calendario_mensaje"),
    
    path('agregar_hora/', agregar_hora, name="agregar_hora"),
    
]
