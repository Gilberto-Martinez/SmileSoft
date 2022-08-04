from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from gestion_cobros.models import CobroContado, DetalleCobroContado, DetalleCobroTratamiento
import gestion_administrativo.models
from gestion_tratamiento.models import Tratamiento
from gestion_administrativo.models import Persona, PacienteTratamientoAsignado, Paciente

def cobrar_tratamiento(request, cedula):
    listado_tratamientos = PacienteTratamientoAsignado.objects.all()
    persona = Persona.objects.get(numero_documento=cedula)
    # paciente = Paciente.objects.get(numero_documento=cedula)
    # id_paciente = paciente.id_paciente

    tratamientos_asignados = []
    precio_total = 0
    id_paciente_tratamiento = ''
    for tratamiento in listado_tratamientos:
        if str(tratamiento.get_paciente()) == str(cedula):
            id_paciente_tratamiento = tratamiento.id
            cod_tratamiento = tratamiento.get_tratamiento()
            nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            precio_total = precio_total + nuevo_tratamieto.precio
            tratamientos_asignados.append(nuevo_tratamieto)

    precio_total = '{:,}'.format(precio_total).replace(',','.')
    edad = persona.obtener_edad()
    menor_edad = False
    if edad > 18:
        menor_edad = True

    return render (request,"cobrar_tratamiento.html",{
                                                        'tratamientos_asignados':tratamientos_asignados,
                                                        'persona':persona,
                                                        'precio_total':precio_total,
                                                        'id_paciente_tratamiento':id_paciente_tratamiento,
                                                        'menor_edad':menor_edad
                                                    }
                    )

def registrar_cobro(request, numero_documento):
    paciente = Paciente.objects.get(numero_documento=numero_documento)
    persona = Persona.objects.get(numero_documento=numero_documento)
    nombre = str(persona.nombre)+" "+str(persona.apellido)
    precio_total = obtener_precio_total(numero_documento)

    cobro_contado = CobroContado.objects.create(
                                        paciente=paciente,
                                        numero_documento= numero_documento,
                                        razon_social=nombre,
                                        monto_total=precio_total
    )

    tratamientos_confirmados = obtener_tratamientos(numero_documento)
    detalle_cobro_nuevo = DetalleCobroContado.objects.create(
                                                        cobro=cobro_contado
    )
    for tratamiento_conf in tratamientos_confirmados:
        DetalleCobroTratamiento.objects.create(
                                            detalle_cobro=detalle_cobro_nuevo,
                                            tratamiento = tratamiento_conf
        )
    confirmar_tratamientos(numero_documento)
    return render(request, "confirmar_cobro.html")

def obtener_tratamientos(cedula):
    listado_tratamientos = PacienteTratamientoAsignado.objects.all()
    tratamientos_asignados = []

    for tratamiento in listado_tratamientos:
        if str(tratamiento.get_paciente()) == str(cedula):
            cod_tratamiento = tratamiento.get_tratamiento()
            nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            tratamientos_asignados.append(nuevo_tratamieto)
    return tratamientos_asignados

def obtener_precio_total(cedula):
    listado_tratamientos = PacienteTratamientoAsignado.objects.all()
    precio_total = 0

    for tratamiento in listado_tratamientos:
        if str(tratamiento.get_paciente()) == str(cedula):
            cod_tratamiento = tratamiento.get_tratamiento()
            nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            precio_total = precio_total + nuevo_tratamieto.precio
    return precio_total

def confirmar_tratamientos(cedula):
    """ 
    Cambia el estado de los tratamientos asignados a un paciente de la siguiente manera:
        Una vez que se haya realizado el registro del cobro de los tratamientos cambia el
        estados de estos a Confirmado, es decir, estado = Confirmado
    """
    paciente = Paciente.objects.get(numero_documento=cedula)
    id_paciente = paciente.id_paciente
    listado_tratamientos = PacienteTratamientoAsignado.objects.all()
    # tratamientos_asignados = []

    for tratamiento in listado_tratamientos:
        if str(tratamiento.get_paciente()) == str(cedula):
            cod_tratamiento = tratamiento.get_tratamiento()
            PacienteTratamientoAsignado.objects.filter(paciente = id_paciente,tratamiento = cod_tratamiento,).update(estado = 'Confirmado')
            print("Se ejecuta")
            print("Se ejecuta")
            print("Se ejecuta")
            print("Se ejecuta")
            print("Se ejecuta")
            # resultado = PacienteTratamientoAsignado.objects.update(
            #                                                 paciente = id_paciente,
            #                                                 tratamiento = cod_tratamiento,
            #                                                 estado = 'Confirmado'
        # )

#---------------------------------------------------------#
class CobrosListView(ListView):
    model = CobroContado
    template_name = 'listar_cobro_contado.html'