from asyncio.windows_events import NULL
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from gestion_administrativo.models import TratamientoConfirmado
from gestion_historial_clinico.models import *
from gestion_administrativo.models import Paciente


def guardar_historial_clinico(id_tratamiento_conf):
    tratamiento_conf = TratamientoConfirmado.objects.get(id_tratamiento_conf=id_tratamiento_conf)
    paciente_id = tratamiento_conf.get_paciente()
    tratamiento_id = tratamiento_conf.get_tratamiento()
    tratamiento = Tratamiento.objects.get(codigo_tratamiento=tratamiento_id)

    paciente = Paciente.objects.get(id_paciente=paciente_id)

    HistorialClinico.objects.create(tratamiento=tratamiento, paciente=paciente)


def listar_pacientes_historial(request):
    lista_historial = HistorialClinico.objects.all()
    lista_paciente_historial = []

    for historial in lista_historial:
        respuesta = ' '
        paciente = Paciente.objects.get(id_paciente=historial.paciente.id_paciente)
        if not lista_paciente_historial: # Condición que comprueba si la lista está vacia
            print('Es nulo')
            lista_paciente_historial.append(paciente)
        else:
            for paciente_hist in lista_paciente_historial:
                if paciente_hist.id_paciente != paciente.id_paciente:
                    respuesta = 'DISTINTOS'
            if respuesta == 'DISTINTOS':
                lista_paciente_historial.append(paciente)

    return render(request,'listar_pacientes_historial.html',{
                                                            'lista_paciente_historial':lista_paciente_historial
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
