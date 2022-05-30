from django.contrib import admin
from django.urls import path
from gestion_sesion import views

urlpatterns = [
    path('home/',views.home),
    path('iniciosesion/', views.iniciosesion, name='iniciosesion'),
    path('inicio/', views.inicio, name='inicio'),
    path('cierre/', views.cierre, name='cierresesion'),
]