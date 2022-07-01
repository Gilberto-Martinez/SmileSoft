"""SmileSoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.urls.resolvers import URLPattern
from webapp import views

urlpatterns = [

    #path de Django Admin
    path('admin/', admin.site.urls),
    #path('', admin.site.urls),
    
    #App Gestion administrativo
    #url que se coloca en navegador ('direccion del archivo urls','identificador del conjunto de url en app')
   # path('administrativo/', include(('gestion_administrativo.urls','administrativo'),)),
    path('administrativo/', include('gestion_administrativo.urls')),
    #path('registro_personas/', include ('gestion_administrativo.urls')) por ejemplo si esto queda así, deberia ser 127.0.0.1:8000/registro_personas/registro_personas,
    
    #App Panel_control
    # path('', include('panel_control.urls')),
    path('panel_control/', include(('panel_control.urls', 'panel_control'),)),
    
    #App WebApp alias gestion de sesion
   # path('sesion/', include(('webapp.urls','sesion'),)),
    path('', include(('webapp.urls', 'sesion'),)),
   
    #App Roles
    path('roles/', include(('gestion_roles.urls', 'roles'),)),

    #App Tratamiento
    path('tratamiento/', include(('gestion_tratamiento.urls', 'tratamiento'),)),
   
    #App Agendamiento
    path('agendamiento/', include(('gestion_agendamiento.urls', 'agendamiento'),)),

    #App Inventario de Insumos
    path('insumo/', include(('gestion_inventario_insumos.urls', 'insumo'),)),

  # path('accounts/', include ('django.contrib.auth.urls')),
   
    
    
    # path('sesion/', include(('gestion_sesion.urls','sesion'),)),
    # path('base/', include( ('gestion_sesion.urls','sesion'))),
    
     
    
    
]
