from django.urls import path
from .views import *

urlpatterns = [
    path('cobrar_tratamiento/<str:cedula>', cobrar_tratamiento, name="cobrar_tratamiento"),
    path('registrar_cobro/<str:numero_documento>/', registrar_cobro, name="registrar_cobro"),
    path('listar_cobros/', CobrosListView.as_view(), name="listar_cobros"),
    # path('calendar/', pruebacalendar, name="calendar"),
]