from django.urls import path
from .views import *

urlpatterns = [
    # path('cobrar_tratamiento/<int:id_paciente>', cobrar_tratamiento, name="cobrar_tratamiento"),
    path('mostrar_tratamientos_cobrar/<int:id_paciente>', mostrar_tratamientos_cobrar, name="mostrar_tratamientos_cobrar"),
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
    path('confirmacion_de_cobro/<int:id_factura>', confirmacion_de_cobro, name="confirmacion_de_cobro"),

    path('ingresar_datos_factura/<int:id_cobro>', ingresar_datos_factura, name="ingresar_datos_factura"),
    path('ingresar_datos_cobro/<int:id_paciente>', ingresar_datos_cobro, name="ingresar_datos_cobro"),
    path('visualizar_datos_factura/<int:id_factura>', visualizar_datos_factura, name="visualizar_datos_factura"),
    
    #Factura_html
    path('generar_factura_original/', generar_factura_original, name="generar_factura_original"),
    path('listar_facturas/', listar_facturas, name="listar_facturas"),
    path('cambiar_estado_factura/<id_factura>', cambiar_estado_factura, name="cambiar_estado_factura"),
    
    #PDF------------------------
    path('detalle_cobro_pdf/<int:id_paciente>', detalle_cobro_pdf ,name="detalle_cobro_pdf"),
    path('presupuesto_pdf/<int:id_paciente>',  presupuesto_pdf, name="presupuesto_pdf"),
    path('generar_factura/<int:id_factura>', generar_factura, name="generar_factura"),

    # Cobranza --------------------
    path('mostrar_caja/<str:numero_documento>', mostrar_caja, name="mostrar_caja"),
    path('datos_apertura_caja/<str:numero_documento>/<str:id_paciente>', guardar_datos_apertura_caja, name="datos_apertura_caja"),
    path('datos_apertura_caja2/<str:numero_documento>', guardar_datos_apertura_caja2, name="datos_apertura_caja2"),
    path('msj_caja_cerrada/<str:id_paciente>/<str:numero_documento>', msj_caja_cerrada, name="msj_caja_cerrada"),
    path('msj_caja_abierta2/', msj_caja_abierta2, name="msj_caja_abierta2"),
    path('cerrar_caja/', cerrar_caja, name="cerrar_caja"),
]