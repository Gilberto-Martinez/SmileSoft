from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from gestion_administrativo.models import TratamientoConfirmado
from gestion_cobros.models import CobroContado, DetalleCobroContado, DetalleCobroTratamiento
from gestion_tratamiento.models import Tratamiento
from gestion_administrativo.models import Persona, PacienteTratamientoAsignado, Paciente

def cobrar_tratamiento(request, id_paciente):
    listado_tratamientos = TratamientoConfirmado.objects.all()
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    # id_paciente = paciente.id_paciente

    tratamientos_asignados = []
    precio_total = 0
    id_tratamiento_confirmado = ''
    for tratamiento in listado_tratamientos:
        if str(tratamiento.get_paciente()) == str(id_paciente):
            id_tratamiento_confirmado = tratamiento.id_tratamiento_conf
            cod_tratamiento = tratamiento.get_tratamiento()
            nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            precio_total = precio_total + nuevo_tratamieto.precio
            tratamientos_asignados.append(nuevo_tratamieto)

    precio_total = '{:,}'.format(precio_total).replace(',','.')
    edad = persona.obtener_edad()
    menor_edad = False
    if edad < 18:
        menor_edad = True

    return render (request,"cobrar_tratamiento.html",{
                                                        'tratamientos_asignados':tratamientos_asignados,
                                                        'persona':persona,
                                                        'precio_total':precio_total,
                                                        'id_tratamiento_confirmado':id_tratamiento_confirmado,
                                                        'menor_edad':menor_edad,
                                                        'id_paciente':id_paciente
                                                    }
                    )

def registrar_cobro(request, numero_documento):
    paciente = Paciente.objects.get(numero_documento=numero_documento)
    persona = Persona.objects.get(numero_documento=numero_documento)
    nombre = str(persona.nombre)+" "+str(persona.apellido)
    precio_total = obtener_precio_total(numero_documento)

    if precio_total>0:
        cobro_contado = CobroContado.objects.create(
                                            paciente=paciente,
                                            numero_documento= numero_documento,
                                            razon_social=nombre,
                                            monto_total=precio_total
        )
    else:
        return redirect("/cobros/error_cobro/")

    tratamientos_confirmados = obtener_tratamientos(numero_documento)
    detalle_cobro_nuevo = DetalleCobroContado.objects.create(
                                                        cobro=cobro_contado,
                                                        # tratamientos=tratamientos_confirmados
    )
    # detalle_actualiado =DetalleCobroContado.objects.filter(cobro=cobro_contado).update()
    for tratamiento_conf in tratamientos_confirmados:
        print("Tratamiento: ",tratamiento_conf.codigo_tratamiento)
        # DetalleCobroContado.objects.filter(cobro=cobro_contado).update(tratamientos=tratamiento_conf)
        detalle_cobro_tratamiento = DetalleCobroTratamiento.objects.create(
                                            detalle_cobro=detalle_cobro_nuevo,
                                            tratamiento = tratamiento_conf
        )
    confirmar_tratamientos(numero_documento)
    return redirect("/cobros/mensaje_confirmacion_cobro/")


def registrar_cobro_pendiente(numero_documento):
    paciente = Paciente.objects.get(numero_documento=numero_documento)
    persona = Persona.objects.get(numero_documento=numero_documento)
    nombre = str(persona.nombre)+" "+str(persona.apellido)
    precio_total = obtener_precio_total(numero_documento)

    if precio_total>0:
        cobro_contado = CobroContado.objects.create(
                                            paciente=paciente,
                                            numero_documento= numero_documento,
                                            razon_social=nombre,
                                            monto_total=precio_total,
                                            estado='Pendiente'
        )
    else:
        return redirect("/cobros/error_cobro/")

    tratamientos_confirmados = obtener_tratamientos(numero_documento)
    detalle_cobro_nuevo = DetalleCobroContado.objects.create(
                                                        cobro=cobro_contado,
                                                        # tratamientos=tratamientos_confirmados
    )
    # detalle_actualiado =DetalleCobroContado.objects.filter(cobro=cobro_contado).update()
    for tratamiento_conf in tratamientos_confirmados:
        print("Tratamiento: ",tratamiento_conf.codigo_tratamiento)
        # DetalleCobroContado.objects.filter(cobro=cobro_contado).update(tratamientos=tratamiento_conf)
        detalle_cobro_tratamiento = DetalleCobroTratamiento.objects.create(
                                            detalle_cobro=detalle_cobro_nuevo,
                                            tratamiento = tratamiento_conf
        )
    confirmar_tratamientos(numero_documento)
    return redirect("/cobros/mensaje_confirmacion_cobro/")


def obtener_tratamientos(cedula):
    listado_tratamientos = PacienteTratamientoAsignado.objects.all()
    tratamientos_asignados = []

    for tratamiento in listado_tratamientos:
        if str(tratamiento.paciente) == str(cedula):
            cod_tratamiento = tratamiento.get_tratamiento()
            print("Este es el tratamiento: ",cod_tratamiento)
            nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            tratamientos_asignados.append(nuevo_tratamieto)
    return tratamientos_asignados

def obtener_precio_total(cedula):
    listado_tratamientos = PacienteTratamientoAsignado.objects.all()
    precio_total = 0
    paciente = Paciente.objects.get(numero_documento=cedula)

    for tratamiento in listado_tratamientos:
        if str(tratamiento.get_paciente()) == str(paciente.id_paciente):
            cod_tratamiento = tratamiento.get_tratamiento()
            nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            precio_total = precio_total + nuevo_tratamieto.precio
    return precio_total

def confirmar_tratamientos(cedula):
    """ 
        Copia el/los registro/s de la tabla PacienteTratamientoAsignado a Tratamiento confirmado
        con estado = confirmado
        Luego elimina el/los registro/s en cuestión de la tabla PacienteTratamientoAsignado
    """
    paciente = Paciente.objects.get(numero_documento=cedula)
    id_paciente = paciente.id_paciente
    listado_tratamientos_asig = PacienteTratamientoAsignado.objects.all()

    for tratamiento_asig in listado_tratamientos_asig:
        if str(tratamiento_asig.get_paciente()) == str(id_paciente):
            tratatmiento_asign = tratamiento_asig.tratamiento
            id_tratamiento_asig = tratamiento_asig.id_tratamiento_asig
            # tratamiento = tratamiento_pagado.tratamiento
            tratamiento_conf = TratamientoConfirmado.objects.create(
                                                                    tratamiento = tratatmiento_asign,
                                                                    paciente = paciente,
                                                                    estado = 'Confirmado'
            )
            tratamiento_pagado = PacienteTratamientoAsignado.objects.filter(id_tratamiento_asig=id_tratamiento_asig).delete()

def ver_detalle_cobro(request, id_cobro_contado):
    cobro = CobroContado.objects.get(id_cobro_contado=id_cobro_contado)
    detalle_cobro = DetalleCobroContado.objects.get(cobro=id_cobro_contado)
    id_detalle_cobro = detalle_cobro.id
    detalle_tratamientos = DetalleCobroTratamiento.objects.all()
    tratamientos =[]

    for detalle_tratamiento in detalle_tratamientos:
        print("id Detalle parametro: ", id_detalle_cobro)
        print("Detalle de cobro en BD: ", detalle_tratamiento.detalle_cobro.id)
        if detalle_tratamiento.detalle_cobro.id == id_detalle_cobro:
            id_tratamiento = detalle_tratamiento.tratamiento.get_codigo_tratamiento()
            tratamiento = Tratamiento.objects.get(codigo_tratamiento=id_tratamiento)
            precio = '{:,}'.format(tratamiento.precio).replace(',','.')
            tratamiento_tmp = {
                                'nombre_tratamiento':tratamiento.nombre_tratamiento,
                                'precio':precio
            }
            tratamientos.append(tratamiento_tmp)
            print("Entra en detalle de cobro")

    monto_total = cobro.monto_total
    monto_total = '{:,}'.format(monto_total).replace(',','.')

    return render(request, 'ver_detalle_cobro.html',{
                                                    'cobro':cobro,
                                                    'tratamientos':tratamientos,
                                                    'monto_total':monto_total
                                                    }
                )

#----------------------------------------------#
def eliminar_tratamiento_confirmado(request, id_tratamiento_confirmado):
    """
    Elimina de la tabla TratamientoConfirmado el registro correspondiente al tratamiento que
    el paciente haya agendado, además cambia el estado de la Cita en 'Pendiente'
    """
    paciente_tratamiento = TratamientoConfirmado.objects.get(id_tratamiento_conf=id_tratamiento_confirmado)
    id_paciente = paciente_tratamiento.paciente.get_id()
    paciente_tratamiento.delete()
    return redirect('/cobros/cobrar_tratamiento/%s'%(id_paciente))

#---------------------------- LISTADOS -----------------------------#

def listar_cobros(request):
    cobros = CobroContado.objects.all()
    listado_cobros = []
    for cobro in cobros:
        monto_total = '{:,}'.format(cobro.monto_total).replace(',','.')
        cobro_tmp = {
                    'id_cobro_contado' : cobro.id_cobro_contado,
                    'numero_documento' : cobro.numero_documento,
					'razon_social' : cobro.razon_social,
					'fecha' : cobro.fecha,
                    'monto_total' :monto_total
        }
        listado_cobros.append(cobro_tmp)

    return render(request, 'listar_cobro_contado.html', {'listado_cobros':listado_cobros})


def listar_cobros_pendientes(request):
    tratamientos_agendados = TratamientoConfirmado.objects.filter(estado='Agendado')
    pacientes = []

    for tratamiento_agen in tratamientos_agendados:
        pacientes.append(tratamiento_agen.paciente)

    return render(request,'listar_cobros_pendientes.html', {'pacientes':pacientes})

#------------------------ Vista de mensajes ----------------------------#
class ErrorCobro(TemplateView):
    template_name = "mensajes/error_cobro.html"

class ConfirmacionCobro(TemplateView):
    template_name = "mensajes/confirmar_cobro.html"

