from datetime import datetime
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView, View
from gestion_tratamiento.models import TratamientoInsumoAsignado
from gestion_inventario_insumos.models import Insumo
from gestion_cobros.utils import render_to_pdf
from django.http import (Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,)
from gestion_administrativo.models import TratamientoConfirmado
from gestion_cobros.models import CobroContado, DetalleCobroContado, DetalleCobroTratamiento
from gestion_tratamiento.models import Tratamiento
from gestion_administrativo.models import Persona, PacienteTratamientoAsignado, Paciente
from gestion_agendamiento.models import Cita
from .forms import RazonSocialForm
from django.db.models import Q
from datetime import datetime
import datetime
def cobrar_tratamiento(request, id_paciente):
    listado_tratamientos = TratamientoConfirmado.objects.filter(estado='Confirmado')
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    # id_paciente = paciente.id_paciente

    tratamientos_agendados = []
    precio_total = 0
    for tratamiento in listado_tratamientos:
        if str(tratamiento.get_paciente()) == str(id_paciente):
            cod_tratamiento = tratamiento.get_tratamiento()
            nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            tratamiento_agendado = {
                                    'tratamiento':nuevo_tratamieto,
                                    'id_tratamiento_confirmado' :tratamiento.id_tratamiento_conf,
                                    'id_cita':tratamiento.id_cita
            }
            precio_total = precio_total + nuevo_tratamieto.precio
            tratamientos_agendados.append(tratamiento_agendado)

    precio_total = '{:,}'.format(precio_total).replace(',','.')
    edad = persona.obtener_edad()
    menor_edad = False
    if edad < 18:
        menor_edad = True

    return render (request,"cobrar_tratamiento.html",{
                                                        'tratamientos_agendados':tratamientos_agendados,
                                                        'persona':persona,
                                                        'precio_total':precio_total,
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

        tratamientos_confirmados = obtener_tratamientos(numero_documento)
        detalle_cobro_nuevo = DetalleCobroContado.objects.create(
                                                            cobro=cobro_contado,
                                                            # tratamientos=tratamientos_confirmados
        )
        # detalle_actualiado =DetalleCobroContado.objects.filter(cobro=cobro_contado).update()
        for tratamiento_conf in tratamientos_confirmados:
            # print("Tratamiento: ",tratamiento_conf.codigo_tratamiento)
            # DetalleCobroContado.objects.filter(cobro=cobro_contado).update(tratamientos=tratamiento_conf)
            detalle_cobro_tratamiento = DetalleCobroTratamiento.objects.create(
                                                detalle_cobro=detalle_cobro_nuevo,
                                                tratamiento = tratamiento_conf
            )
        pagar_tratamientos(numero_documento)
    
    else:
        return redirect("/cobros/error_cobro/")

    return redirect("/cobros/mensaje_confirmacion_cobro/")


def registrar_cobro2(request, numero_documento, numero_documento2,razon_social):
    paciente = Paciente.objects.get(numero_documento=numero_documento)
    precio_total = obtener_precio_total(numero_documento)

    if precio_total>0:
        cobro_contado = CobroContado.objects.create(
                                                paciente=paciente,
                                                numero_documento= numero_documento2,
                                                razon_social=razon_social,
                                                monto_total=precio_total
                                            )

        tratamientos_confirmados = obtener_tratamientos(numero_documento)
        detalle_cobro_nuevo = DetalleCobroContado.objects.create(
                                                            cobro=cobro_contado,
                                                            # tratamientos=tratamientos_confirmados
        )
        # detalle_actualiado =DetalleCobroContado.objects.filter(cobro=cobro_contado).update()
        for tratamiento_conf in tratamientos_confirmados:
            # print("Tratamiento: ",tratamiento_conf.codigo_tratamiento)
            # DetalleCobroContado.objects.filter(cobro=cobro_contado).update(tratamientos=tratamiento_conf)
            detalle_cobro_tratamiento = DetalleCobroTratamiento.objects.create(
                                                detalle_cobro=detalle_cobro_nuevo,
                                                tratamiento = tratamiento_conf
            )
        pagar_tratamientos(numero_documento)
    
    else:
        return redirect("/cobros/error_cobro/")

    return redirect("/cobros/mensaje_confirmacion_cobro/")


def verificar_datos_cita(request, numero_documento, menor_edad):
    """
    Verifica los siguientes datos:
        -Si la persona (paciente en cuestion) es mayor de edad, en caso contrario se solicitará ingresar el nombre de la razon social
        -Que la fecha agendada sea mayor o igual a la fecha actual, en caso contrario muestra mensajes de error
        -Que la hora agendada (si fecha agendad = fecha actual) sea mayor a la hora actual, en caso contrario muestra mensajes de error 
    """

    paciente = Paciente.objects.get(numero_documento=numero_documento)
    tratamientos_conf = TratamientoConfirmado.objects.all()
    now = datetime.now()
    fecha_actual = now.date()
    hora_actual = now.time()
    respuesta = False
    for tratamiento_conf in tratamientos_conf:
        if tratamiento_conf.paciente.id_paciente == paciente.id_paciente and tratamiento_conf.estado == 'Confirmado':
            id_cita = tratamiento_conf.id_cita
            cita = Cita.objects.get(id_cita=id_cita)
            if cita.fecha > fecha_actual:
                respuesta = True
            else:
                if cita.fecha == fecha_actual:
                    if cita.hora_atencion.hora > hora_actual:
                        respuesta = True
                    else:
                        return render(request, 'mensajes/error_hora_pasada.html',{'id_cita':id_cita})
                else:
                    return render(request, 'mensajes/error_fecha_pasada.html',{'id_cita':id_cita})

    if respuesta == True:
        if menor_edad is True:
            return redirect("/cobros/solicitar_razon_social/%s" (numero_documento))
        return redirect("/cobros/registrar_cobro/%s" %(numero_documento))
        

    print('respuesta: ',respuesta)
    return render(request, 'mensajes/pagina_error.html')

def solicitar_razon_social(request, numero_documento):
    data ={
            'form':RazonSocialForm()
    }

    if request.method == 'POST':
        form = RazonSocialForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            datos = form.save(commit=False)
            razon_social = datos.razon_social
            numero_documento2 = datos.numero_documento
            return redirect('/cobros/registrar_cobro2/%s/%s/%s' %(numero_documento, numero_documento2, razon_social))

    return render('solicitar_razon_social.html', data)


# def registrar_cobro_pendiente(numero_documento):
#     paciente = Paciente.objects.get(numero_documento=numero_documento)
#     persona = Persona.objects.get(numero_documento=numero_documento)
#     nombre = str(persona.nombre)+" "+str(persona.apellido)
#     precio_total = obtener_precio_total(numero_documento)

#     if precio_total>0:
#         cobro_contado = CobroContado.objects.create(
#                                             paciente=paciente,
#                                             numero_documento= numero_documento,
#                                             razon_social=nombre,
#                                             monto_total=precio_total,
#                                             estado='Pendiente'
#         )
#     else:
#         return redirect("/cobros/error_cobro/")

#     tratamientos_confirmados = obtener_tratamientos(numero_documento)
#     detalle_cobro_nuevo = DetalleCobroContado.objects.create(
#                                                         cobro=cobro_contado,
#                                                         # tratamientos=tratamientos_confirmados
#     )
#     # detalle_actualiado =DetalleCobroContado.objects.filter(cobro=cobro_contado).update()
#     for tratamiento_conf in tratamientos_confirmados:
#         print("Tratamiento: ",tratamiento_conf.codigo_tratamiento)
#         # DetalleCobroContado.objects.filter(cobro=cobro_contado).update(tratamientos=tratamiento_conf)
#         detalle_cobro_tratamiento = DetalleCobroTratamiento.objects.create(
#                                             detalle_cobro=detalle_cobro_nuevo,
#                                             tratamiento = tratamiento_conf
#         )
#     pagar_tratamientos(numero_documento)
#     return redirect("/cobros/mensaje_confirmacion_cobro/")


def obtener_tratamientos(cedula):
    listado_tratamientos = TratamientoConfirmado.objects.filter(estado='Confirmado')
    tratamientos_asignados = []

    for tratamiento in listado_tratamientos:
        if str(tratamiento.paciente.numero_documento) == str(cedula):
            cod_tratamiento = tratamiento.get_tratamiento()
            # print("Este es el tratamiento: ",cod_tratamiento)
            nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            tratamientos_asignados.append(nuevo_tratamieto)
    return tratamientos_asignados

def obtener_precio_total(cedula):
    listado_tratamientos = TratamientoConfirmado.objects.filter(estado='Confirmado')
    precio_total = 0
    paciente = Paciente.objects.get(numero_documento=cedula)

    for tratamiento in listado_tratamientos:
        if str(tratamiento.get_paciente()) == str(paciente.id_paciente):
            cod_tratamiento = tratamiento.get_tratamiento()
            nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            precio_total = precio_total + nuevo_tratamieto.precio
    return precio_total

def pagar_tratamientos(cedula):
    """ 
        Cambia el estado de la tabla TratamientoConfirmado
        con estado = 'Pagado'
    """
    paciente = Paciente.objects.get(numero_documento=cedula)
    id_paciente = paciente.id_paciente
    listado_tratamientos_conf = TratamientoConfirmado.objects.filter(estado='Confirmado')

    for tratamiento_conf in listado_tratamientos_conf:
        if str(tratamiento_conf.paciente.id_paciente) == str(id_paciente):
            id_tratamiento_con = tratamiento_conf.id_tratamiento_conf
            tratamiento_pag = TratamientoConfirmado.objects.filter(id_tratamiento_conf=id_tratamiento_con).update(estado='Pagado')


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
    En tabla TratamientoConfirmado el registro correspondiente al tratamiento que
    el paciente haya decidido no pagar (y selecciona en Eliminar), cambia el estado del 
    TratamientoConfirmado 'Agendado' y el estado de la Cita en 'Pendiente'
    """
    tratamiento_conf = TratamientoConfirmado.objects.get(id_tratamiento_conf=id_tratamiento_confirmado) #Obtiene una instancia de TratamientoConfirmado
    id_paciente = tratamiento_conf.paciente.get_id()
    tratamiento_act = TratamientoConfirmado.objects.filter(id_tratamiento_conf=id_tratamiento_confirmado) #Filtra un registro de la tabla Tratamiento confirmado para luego actualizarlo
    tratamiento_act.update(estado='Agendado') # Realiza una actualización del registro obtenido en la fila de arriba
    cita = Cita.objects.filter(id_cita=tratamiento_conf.id_cita).update(estado=False) #Filtra un registro de la tabla Cita y lo actualiza
    return redirect('/cobros/cobrar_tratamiento/%s'%(id_paciente))

#---------------------------- LISTADOS -----------------------------#

def listar_cobros(request):
    busqueda = request.POST.get("q")
      #'filtro de fecha, y nombre 
    filtro = request.POST.get("f")
    
    cobros = CobroContado.objects.all()
    if filtro:
            print("Buscado AQUI", filtro)
            cobros = CobroContado.objects.filter(
                Q(fecha__icontains=filtro))

    elif busqueda:
        cobros = CobroContado.objects.filter(
                Q(razon_social__icontains=busqueda))
  
    # cobros = CobroContado.objects.all()
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
    tratamientos_agendados = TratamientoConfirmado.objects.filter(estado='Confirmado')
    pacientes = Paciente.objects.all()
   
    busqueda = request.POST.get("q")
    #'filtro de nombre
  
    if busqueda:
        pacientes = Paciente.objects.filter(
           Q(numero_documento__nombre__icontains=busqueda))
        print('Busca', busqueda)
    
    
    lista_pacientes = []

    for paciente in pacientes:
        for tratamiento_agen in tratamientos_agendados:
            if paciente.id_paciente == tratamiento_agen.paciente.id_paciente:
                print("En paciente: ",paciente.id_paciente, 'En Tratamiento Confirmado: ',tratamiento_agen.paciente.id_paciente )
                print('#--------------------#')
                lista_pacientes.append(paciente)
                break

    return render(request,'listar_cobros_pendientes.html', {'pacientes':lista_pacientes})




#------------------PDF-------------------------------------------------#

def detalle_cobro_pdf(request, id_paciente):
    listado_tratamientos = TratamientoConfirmado.objects.filter(estado='Confirmado')
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    fecha_actual= (datetime.datetime.now().strftime('%d/%m/%Y'))
   
    listado_insumos_asig= TratamientoInsumoAsignado.objects.all()
    
    tratamientos_insumos_asignados = []
    
    precio_total = 0
    insumos=[]
    
    for tratamiento in listado_tratamientos:
        if str(tratamiento.get_paciente()) == str(id_paciente):
            cod_tratamiento = tratamiento.get_tratamiento()
            nuevo_tratamiento = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            nuevo_insumo= []
            # fecha_actual= datetime.datetime.now().strftime('%d/%m/%Y')
            
            for insumo_asig in listado_insumos_asig:
                if str(insumo_asig.get_tratamiento()) == str(cod_tratamiento):
                    # id_tratamiento_insumo = tratamiento.id_insumo_asig
                    cod_insumo = insumo_asig.get_insumo()
                    nuevo_insumo = Insumo.objects.get(codigo_insumo=cod_insumo)
                    insumos.append(nuevo_insumo)
                    # print("Tratamiento: "," ", nuevo_tratamiento.nombre_tratamiento,", INSUMO: ", nuevo_insumo.nombre_insumo)
            tratamiento_insumo_asig = {
                                        "insumos":insumos,
                                        
                                        "tratamiento":nuevo_tratamiento
            }
            tratamientos_insumos_asignados.append(tratamiento_insumo_asig)
            print("Listado de Tratamientos con Insumo",{'tratamientos_insumos_asignados':tratamientos_insumos_asignados })
      
            precio_total = int(precio_total) + int(nuevo_tratamiento.precio)
            # tratamientos_agendados.append(tratamiento_agendado)

            # precio_total = '{:,}'.format(precio_total).replace(',','.')
        
    pdf = render_to_pdf("detalle_cobro_pdf.html",{
                                                    'tratamientos_insumos_asignados': tratamientos_insumos_asignados,
                                                    'persona':persona,
                                                    'fecha_actual': fecha_actual,
                                                    'precio_total':precio_total,
                                                    
                                                })
    return HttpResponse(pdf, content_type='application/pdf')





#--PDF2--PRESUPUESTO---------------------------------------------------#
def presupuesto_pdf(request, id_paciente):
    # listado_tratamientos = TratamientoConfirmado.objects.filter(
    #     estado='Confirmado')
    listado_tratamientos_asig = PacienteTratamientoAsignado.objects.all()
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    fecha_actual = (datetime.datetime.now().strftime('%d/%m/%Y'))

    listado_insumos_asig = TratamientoInsumoAsignado.objects.all()
    tratamientos_insumos_asignados = []
    precio_total = 0
    
    
    tratamientos_asignados = []
    id_paciente_tratamiento = ''

    for tratamiento_asig in listado_tratamientos_asig:
        if str(tratamiento_asig.get_paciente()) == str(id_paciente):
            id_paciente_tratamiento = tratamiento_asig.id_tratamiento_asig
            cod_tratamiento = tratamiento_asig.get_tratamiento()
            nuevo_tratamiento = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            nuevo_insumo = []
            insumos = []
            # fecha_actual= datetime.datetime.now().strftime('%d/%m/%Y')

            for insumo_asig in listado_insumos_asig:
                if str(insumo_asig.get_tratamiento()) == str(cod_tratamiento):
                    # id_tratamiento_insumo = tratamiento.id_insumo_asig
                    cod_insumo = insumo_asig.get_insumo()
                    nuevo_insumo = Insumo.objects.get(codigo_insumo=cod_insumo)
                    insumos.append(nuevo_insumo)
                    # print("Tratamiento: "," ", nuevo_tratamiento.nombre_tratamiento,", INSUMO: ", nuevo_insumo.nombre_insumo)
            tratamiento_insumo_asig = {
                "insumos": insumos,

                "tratamiento_asig": nuevo_tratamiento
            }
            tratamientos_insumos_asignados.append(tratamiento_insumo_asig)
            # print("Listado de Tratamientos con Insumo", {
            #         'tratamientos_insumos_asignados': tratamientos_insumos_asignados})

            precio_total = int(precio_total) + int(nuevo_tratamiento.precio)

    pdf = render_to_pdf("presupuesto_pdf.html", {
        'tratamientos_insumos_asignados': tratamientos_insumos_asignados,
        'persona': persona,
        'fecha_actual': fecha_actual,
        'precio_total': precio_total,

    })
    return HttpResponse(pdf, content_type='application/pdf')
#------------------------ Vista de mensajes ----------------------------#
class ErrorCobro(TemplateView):
    template_name = "mensajes/error_cobro.html"

class ConfirmacionCobro(TemplateView):
    template_name = "mensajes/confirmacion_de_cobro.html"

