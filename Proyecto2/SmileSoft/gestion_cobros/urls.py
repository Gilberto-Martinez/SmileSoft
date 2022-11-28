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

    path('ingresar_datos_factura/<int:id_cobro>', ingresar_datos_factura, name="ingresar_datos_factura"),
    path('visualizar_datos_factura/<int:id_factura>', visualizar_datos_factura, name="visualizar_datos_factura"),
    
    #Factura_html
    path('generar_factura_original/', generar_factura_original, name="generar_factura_original"),
    path('listar_facturas/', listar_facturas, name="listar_facturas"),
    path('cambiar_estado_factura/<id_factura>', cambiar_estado_factura, name="cambiar_estado_factura"),
    
    #PDF------------------------
    path('detalle_cobro_pdf/<int:id_paciente>', detalle_cobro_pdf ,name="detalle_cobro_pdf"),
    path('presupuesto_pdf/<int:id_paciente>',  presupuesto_pdf, name="presupuesto_pdf"),
    path('generar_factura/<int:id_factura>', generar_factura, name="generar_factura"),
]