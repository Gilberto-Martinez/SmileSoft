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

# /* Paginas de inicio para el INVITADO*/
def registrese(request):
    return render(request, "panel_control/registrarse.html")

def invitado(request):
    return render (request, "panel_control/invitado.html")

def contacto(request):
    return render (request, "panel_control/contacto.html")

def ortodoncia(request):
    return render(request, "panel_control/ortodoncia.html")


def corona_dental(request):
    return render(request, "panel_control/corona_dental.html")


def blanqueamiento(request):
    return render(request, "panel_control/blanqueamiento.html")

def extracciones(request):
    return render(request, "panel_control/extracciones.html")

def mostrar_pagina_error(request):
    return render(request, "mensajes/pagina_error.html")

def mostrar_mensaje(request,titulo , mensaje):
    return render(request, "mensajes/mostrar_mensaje.html", {
                                                            'titulo':titulo,
                                                            'mensaje':mensaje,
                                                            }
                )




