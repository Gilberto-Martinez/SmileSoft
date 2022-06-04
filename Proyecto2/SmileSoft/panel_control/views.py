from django.shortcuts import render

# Create your views here.

def panel_control(request):
    return render(request, "panel_control/panel_control.html")

def gestion_roles(request):
    return render(request, "panel_control/gestion_roles.html")

def gestion_administrativo(request):
    return render(request, "panel_control/gestion_administrativo.html")

def gestion_tratamiento(request):
    return render(request, "panel_control/gestion_tratamiento.html")


def error(request):
    return render(request, "panel_control/error.html")

def cambio_exitoso(request):
    return render(request, "panel_control/cambio_exitoso.html")
