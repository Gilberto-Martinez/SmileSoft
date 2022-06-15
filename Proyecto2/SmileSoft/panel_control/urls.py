from django.urls import path
from .import views

urlpatterns= [
    # path ('base/', views.panel_control, name="panel_control"),
    path ('inicio/', views.panel_control, name="panel_control"),
    path('error/', views.error, name="panel_control"),
    path('cambio_exitoso/', views.cambio_exitoso, name="panel_control"),
    
    path('registrarse/', views.registrese, name="registrarse"),
    path('invitado/', views.invitado, name="panel_control"),
    path('contacto/', views.contacto, name="panel_control"),
    path('ortodoncia/', views.ortodoncia, name="ortodoncia"),
    path('corona_dental/', views.corona_dental, name=" corona_dental"),
    path('blanqueamiento/', views.blanqueamiento, name="blanqueamiento"),
    path('extracciones/', views.extracciones, name="extracciones"),
    
    # path('gestion_roles/', views.gestion_roles , name="gestion_roles"),
    # path('gestion_administrativo/', views.gestion_administrativo, name="gestion_administrativo"),
    # path('gestion_tratamiento/', views.gestion_tratamiento, name="gestion_tratamiento"),
]