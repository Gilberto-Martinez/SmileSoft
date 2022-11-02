from asyncio.windows_events import NULL
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from gestion_administrativo.models import TratamientoConfirmado
from gestion_historial_clinico.models import *
from gestion_administrativo.models import Paciente
from django.contrib.auth.decorators import login_required, permission_required

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

def guardar_historial_clinico(id_tratamiento_conf):
    tratamiento_conf = TratamientoConfirmado.objects.get(id_tratamiento_conf=id_tratamiento_conf)
    paciente_id = tratamiento_conf.get_paciente()
    tratamiento_id = tratamiento_conf.get_tratamiento()
    especialista_id = tratamiento_conf.especialista

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

@permission_required('gestion_historial_clinico.ver_mi_historial_clinico', login_url="/panel_control/error/")
def ver_mi_historial_clinico(request, numero_documento):
    paciente = Paciente.objects.get(numero_documento=numero_documento)
    historial = HistorialClinico.objects.filter(paciente=paciente)

    return render(request, 'ver_historial_clinico.html',{
                                                            'historial':historial,
                                                            'paciente':paciente
                                                            }
            )

