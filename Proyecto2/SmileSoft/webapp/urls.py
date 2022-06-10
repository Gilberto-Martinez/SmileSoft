from django import views
from django.urls import path
# from django.urls.resolvers import URLPattern
from .views import *
#para el reseteo de PASS
from django.contrib.auth import views as auth_views

urlpatterns = [
            # Urls USUARIO
            path('agregar_usuario/', agregar_usuario, name="agregar_usuario"),
            path('modificar_usuario/<usuario>/', modificar_usuario, name="modificar_usuario"),
            path('listar_usuario/', listar_usuario, name="listar_usuario"),
            path('eliminar_usuario/<usuario>/', eliminar_usuario, name="eliminar_usuario"),
            # path('estado_usuario/', estado_usuario, name="estado_usuario"),
            path('modificar_password/', UsuarioView.as_view(), name='modificar_password'),
            path('cambiar_password_usuario/<usuario>/', cambiar_password_usuario, name='cambiar_password_usuario'),

            # Urls de Inicio
            path('login/', inicio_login, name='iniciologin'),
            path('', inicio_login, name='iniciologin'),
            path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
            #----------------------------------------------------------------
            #Url de registrar USUARIO paciente
            path('registrologinpaciente/<str:cedula>', registrologin,
                    name='registrologinpaciente'),
            # path('consultar_documento/', consultar_cedula,name='consultar_documento'),
            path('consultar_documento/', CedulaConsultaView.as_view(),name='consultar_documento'),
            path('mensaje/', MensajeView.as_view(),name='mostrar_mensaje'),
            path('mensaje_confirmacion/<str:cedula>', mostrar_mensaje_confirmacion,name='mostrar_mensaje_confirmacion'),
            # path('mensaje_confirmacion/<str:cedula>', Mensaje_confirmacion.as_view(),name='mostrar_mensaje_confirmacion'),
            path('confirmacion_usuario/', UsuarioConfirmacionView.as_view(),name='confirmacion_usuario'),
            path('generar_usuario_paciente/<str:cedula>', generar_usuario_paciente,name='generar_usuario_paciente'),
            # path('mensaje_envio_correo/', MensajeCorreoView.as_view(),name='mensaje_envio_correo'),

            #  path('registropaciente/', registropaciente, name='registropaciente'), 
            #   path('registro/', FormInvitadoCreate.as_view(),
            #             name="registro_invitado"),

          #----------------------------------------------------------------
          # path('recuperar_pass/', recuperar_pass, name='recuperar_pass'),
          # path('enviarcorreo/', enviarcorreo, name='enviarcorreo'),
            path('recuperar_pass/',  ResetPasswordView.as_view(),name='recuperar_pass'),
            path('password_reset_hecho/',
                  auth_views.PasswordResetDoneView.as_view(
                  template_name='inicio/password_reset_hecho.html')),
]
    
   