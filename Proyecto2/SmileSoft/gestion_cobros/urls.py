from django.urls import path
from .views import *

urlpatterns = [
    path('cobrar_tratamiento/<int:id_paciente>', cobrar_tratamiento, name="cobrar_tratamiento"),
    path('registrar_cobro/<str:numero_documento>/', registrar_cobro, name="registrar_cobro"),
    path('listar_cobros/', CobrosListView.as_view(), name="listar_cobros"),
    # path('calendar/', pruebacalendar, name="calendar"),
    path('error_cobro/', ErrorCobro.as_view(), name="error_cobro"),
    path('mensaje_confirmacion_cobro/', ConfirmacionCobro.as_view(), name="mensaje_confirmacion_cobro"),
    
]