from django.urls import path
from .views import *

urlpatterns = [
    path('cobrar_tratamiento/<int:id_paciente>', cobrar_tratamiento, name="cobrar_tratamiento"),
    path('registrar_cobro/<str:numero_documento>/', registrar_cobro, name="registrar_cobro"),
    path('listar_cobros/', listar_cobros, name="listar_cobros"),
    path('listar_cobros_pendientes/', listar_cobros_pendientes, name="listar_cobros_pendientes"),
    path('eliminar_tratamiento_confirmado/<id_tratamiento_confirmado>', eliminar_tratamiento_confirmado, name="eliminar_tratamiento_confirmado"),
    path('error_cobro/', ErrorCobro.as_view(), name="error_cobro"),
    # path('mensaje_confirmacion_cobro/', ConfirmacionCobro.as_view(), name="mensaje_confirmacion_cobro"),
    path('mensaje_confirmacion_cobro/<id_cobro>', mostrar_msj_confirmacion_cobro, name="mensaje_confirmacion_cobro"),
    path('ver_detalle_cobro/<int:id_cobro_contado>', ver_detalle_cobro, name="ver_detalle_cobro"),
    path('verificar_datos_cita/<numero_documento>/<menor_edad>', verificar_datos_cita, name="verificar_datos_cita"),
    path('solicitar_razon_social/<numero_documento>', solicitar_razon_social, name="solicitar_razon_social"),
    path('registrar_cobro2/<numero_documento>/<numero_documento2>/<razon_social>', registrar_cobro2, name="registrar_cobro2"),
    path('ingresar_datos_factura/<id_cobro>', ingresar_datos_factura, name="ingresar_datos_factura"),
    # path('detalle_cobro_pdf/<int:id_paciente>', DetalleCobroPDF.as_view(),name="detalle_cobro_pdf"),
    path('detalle_cobro_pdf/<int:id_paciente>', detalle_cobro_pdf ,name="detalle_cobro_pdf"),
]