from django import views
from django.urls import path, re_path
from .views import *
from django.contrib.auth import views as auth_views
from .gmail import enviar_link_reseteo

urlpatterns = [
            # Urls USUARIO
            path('agregar_usuario/', agregar_usuario, name="agregar_usuario"),
            path('elegir_persona/', elegir_persona, name="elegir_persona"),
            path('modificar_usuario/<usuario>/', modificar_usuario, name="modificar_usuario"),
            path('listar_usuario/', listar_usuario, name="listar_usuario"),
            path('eliminar_usuario/<usuario>/', eliminar_usuario, name="eliminar_usuario"),
            path('modificar_password/', UsuarioView.as_view(), name='modificar_password'),
            path('cambiar_password_usuario/<usuario>/', cambiar_password_usuario, name='cambiar_password_usuario'),

            # Urls de Inicio
            path('login/', inicio_login, name='iniciologin'),
            path('', inicio_login, name='iniciologin'),
            path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
            path('password_reset/<str:cedula>', resetear_password, name='password_reset'),
            path('recuperar_password/', CedulaConsultaView2.as_view(), name='recuperar_password'),
            path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

            #----------------------------------------------------------------
            #Url de registrar USUARIO paciente
            path('registrologinpaciente/<str:cedula>', registrologin,
                    name='registrologinpaciente'),
            path('consultar_documento/', CedulaConsultaView.as_view(),name='consultar_documento'),
            path('mensaje/', MensajeView.as_view(),name='mensaje'),
            path('mensaje_respuesta/', MensajeView2.as_view(),name='mensaje_respuesta'),
            path('mensaje_confirmacion/<str:cedula>', mostrar_mensaje_confirmacion,name='mostrar_mensaje_confirmacion'),
            path('confirmacion_usuario/<str:cedula>', mostrar_confirmacion_usuario,name='confirmacion_usuario'),
            path('generar_usuario_paciente/<str:cedula>', generar_usuario_paciente,name='generar_usuario_paciente'),
            path('generar_password/<str:cedula>', generar_password,name='generar_password'),
            path('enviar_correo/', enviar_correo,name='enviar_correo'),
            path('enviar_correo_reset/', enviar_link_reseteo,name='enviar_correo_reset'),

          #----------------------------------------------------------------
            path('recuperar_pass/',  ResetPasswordView.as_view(),name='recuperar_pass'),
            path('password_reset_hecho/',
                  auth_views.PasswordResetDoneView.as_view(
                  template_name='inicio/password_reset_hecho.html')),
]