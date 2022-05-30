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
           path('estado_usuario/', estado_usuario, name="estado_usuario"),
           path('modificar_password/', UsuarioView.as_view(), name='modificar_password'),

          # Urls de Inicio
          path('login/', inicio_login, name='iniciologin'),
          path('', inicio_login, name='iniciologin'),
          path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
          #----------------------------------------------------------------
          #Url de registrar USUARIO paciente
          path('registrologinpaciente/<str:cedula>', registrologin,
                    name='registrologinpaciente'),

          #  path('registropaciente/', registropaciente, name='registropaciente'),
          path('registropaciente/', FormPacienteCreate.as_view(),
                    name="registropaciente"),



          #----------------------------------------------------------------
          # path('recuperar_pass/', recuperar_pass, name='recuperar_pass'),
          # path('enviarcorreo/', enviarcorreo, name='enviarcorreo'),
          path('recuperar_pass/',  ResetPasswordView.as_view(),
                    name='recuperar_pass'),
          path('password_reset_hecho/',
                    auth_views.PasswordResetDoneView.as_view(
                        template_name='inicio/password_reset_hecho.html')),
    #----------------------------------------------------------------

]
    
   