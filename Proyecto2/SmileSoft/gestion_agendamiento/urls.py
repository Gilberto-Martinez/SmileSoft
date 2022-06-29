from django.urls import path

from .views import *


urlpatterns = [
    
    # path("calendario/", views.CalendarView.as_view(), name="calendario"),
    path('calendario/', calendario, name="calendario"),
    path('agregar_cita/', agregar_cita, name="agregar_cita"),
]
