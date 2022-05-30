from django.urls import path
from .views import *

urlpatterns = [
            path('listar_roles/', listar_roles, name="listar_roles"),
            path('eliminar_rol/<name>/', eliminar_rol, name="eliminar_rol"),
            path('agregar_roles/', agregar_rol, name="agregar_roles"),
            path('modificar_rol/<name>/', modificar_rol, name="modificar_rol"),
            #path('gestion_roles/',agregar_rol),            
          #   path('agregar_roles/', RolCreate.as_view(),
          #        name="agregar_roles"),



]