from asyncio.windows_events import NULL
from gestion_historial_clinico.utils import render_to_pdf
from django.http import (HttpResponse,)
from gestion_administrativo.models import Persona
from gestion_administrativo.models import TratamientoConfirmado
from gestion_historial_clinico.models import *
from gestion_administrativo.models import Paciente
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from datetime import datetime as class_datetime
import datetime


def guardar_historial_clinico(id_tratamiento_conf):
    tratamiento_conf = TratamientoConfirmado.objects.get(id_tratamiento_conf=id_tratamiento_conf)
    paciente_id = tratamiento_conf.get_paciente()
    tratamiento_id = tratamiento_conf.get_tratamiento()
    especialista_id = tratamiento_conf.especialista.id_especialista_salud

    tratamiento = Tratamiento.objects.get(codigo_tratamiento=tratamiento_id)
    paciente = Paciente.objects.get(id_paciente=paciente_id)
    especialista = EspecialistaSalud.objects.get(id_especialista_salud=especialista_id)

    HistorialClinico.objects.create(
                                    tratamiento=tratamiento, 
                                    paciente=paciente,
                                    especialista=especialista
                                    )


def listar_pacientes_historial(request):
    lista_historial = HistorialClinico.objects.distinct('paciente')
    lista_pacientes = []
    for historial in lista_historial:
        paciente = Paciente.objects.get(id_paciente=historial.paciente.get_id())
        lista_pacientes.append(paciente)

    return render(request,'listar_pacientes_historial.html',{
                                                            'lista_pacientes':lista_pacientes
                                                            }
            )


def listar_historial_clinico(request, id_paciente):
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    historial = HistorialClinico.objects.filter(paciente=paciente)

    return render(request, 'listar_historial_clinico.html',{
                                                            'historial':historial,
                                                            'paciente':paciente
                                                            }
            )


def ver_mi_historial_clinico(request, numero_documento):
   
    try:
        paciente = Paciente.objects.get(numero_documento=numero_documento)
        historial = HistorialClinico.objects.filter(paciente=paciente)
        
    except Paciente.DoesNotExist:
        titulo = '¡Atención!'
        mensaje = 'No es un Paciente, por lo tanto no puede ver esta sección.'
        return redirect('/panel_control/mostrar_mensaje/%s/%s'%(titulo,mensaje))
    return render(request, 'ver_mi_historial_clinico.html',{
                                                            'historial':historial,
                                                            'paciente':paciente
                                                            }
            )


def permiso_mensaje(request,titulo , mensaje):
    return render(request, "permiso_mensaje.html", {
                                                            'titulo':titulo,
                                                            'mensaje':mensaje,
                                                            }
                )


def pdf_historial_clinico(request,id_paciente ):
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    # historial = HistorialClinico.objects.filter(paciente=paciente)
    fecha_actual= (datetime.datetime.now().strftime('%d/%m/%Y'))
    historial = HistorialClinico.objects.filter(paciente=paciente)
    # lista_pacientes = []
    # # for historial in lista_historial:
    # #     paciente = Paciente.objects.get(id_paciente=historial.paciente.get_id())
    # #     lista_pacientes.append(paciente)
    
    pdf = render_to_pdf("pdf_historial_clinico.html", {
                                                        'historial':historial,
                                                        'paciente':paciente,
                                                        'persona':persona,
                                                        'fecha_actual': fecha_actual,
                                                    })
    
    return HttpResponse(pdf, content_type='application/pdf')
