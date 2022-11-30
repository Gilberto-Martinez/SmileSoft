from django.urls import path

from gestion_reporte.views import *

urlpatterns = [
    #Reportes
    path('reporte_tratamiento/', ReporteTratamientoView.as_view(), name='reporte_tratamiento'),
    
    # path("reporte_tratamiento/", tratamiento_reporte , name="reporte_tratamiento "),
    
    path('tratamiento_cita/', ListadoTratamientoView.as_view(), name='tratamiento_cita'),
    
    
    
    path('tratamiento_mas_solicitado/', tratamiento_mas_solicitado, name='tratamiento_mas_solicitado'),
    
     path('insumos_reporte/', insumos_reporte, name='insumos_reporte'),
     
    #Estado de Citas
    path('reporte_cita/', reporte_cita, name='reporte_cita'),
    path('pdf_reporte_cita/', pdf_reporte_cita, name='pdf_reporte_cita'),
    ###
    
    path('cita_reporte/', cita_reporte, name='cita_reporte'),
        
    path('apuntes_graficos/', apuntes_graficos, name='apuntes_graficos'),
   
   
]
