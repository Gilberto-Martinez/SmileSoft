from django.urls import path

from gestion_reporte.views import *

urlpatterns = [
    #Reportes
    path('reporte_tratamiento/', ReporteTratamientoView.as_view(), name='reporte_tratamiento'),
  
    path('tratamiento_cita/', ListadoTratamientoView.as_view(), name='tratamiento_cita'),
    
    
    
    path('tratamiento_mas_solicitado/', tratamiento_mas_solicitado, name='tratamiento_mas_solicitado'),
]
