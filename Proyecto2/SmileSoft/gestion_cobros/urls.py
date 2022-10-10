from django.urls import path
from .views import *

urlpatterns = [
    path('cobrar_tratamiento/<int:id_paciente>', cobrar_tratamiento, name="cobrar_tratamiento"),
    path('registrar_cobro/<str:numero_documento>/', registrar_cobro, name="registrar_cobro"),
    path('listar_cobros/', listar_cobros, name="listar_cobros"),
    path('listar_cobros_pendientes/', listar_cobros_pendientes, name="listar_cobros_pendientes"),
    path('eliminar_tratamiento_confirmado/<id_tratamiento_confirmado>', eliminar_tratamiento_confirmado, name="eliminar_tratamiento_confirmado"),
    # path('calendar/', pruebacalendar, name="calendar"),
    path('error_cobro/', ErrorCobro.as_view(), name="error_cobro"),
    path('mensaje_confirmacion_cobro/', ConfirmacionCobro.as_view(), name="mensaje_confirmacion_cobro"),
    path('ver_detalle_cobro/<int:id_cobro_contado>', ver_detalle_cobro, name="ver_detalle_cobro"),
]