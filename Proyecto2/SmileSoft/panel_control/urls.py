from django.urls import path
from .import views

urlpatterns= [
    # path ('base/', views.panel_control, name="panel_control"),
    path ('inicio/', views.panel_control, name="panel_control"),
    # path('gestion_roles/', views.gestion_roles , name="gestion_roles"),
    # path('gestion_administrativo/', views.gestion_administrativo, name="gestion_administrativo"),
    # path('gestion_tratamiento/', views.gestion_tratamiento, name="gestion_tratamiento"),
]