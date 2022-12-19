
#from datetime import datetime
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from gestion_administrativo.models import Empresa, Funcionario, TratamientoConfirmado
from gestion_tratamiento.models import TratamientoInsumoAsignado
from gestion_inventario_insumos.models import Insumo
from gestion_cobros.utils import render_to_pdf
from django.http import ( HttpResponse,)
from gestion_administrativo.models import TratamientoConfirmado
from gestion_cobros.models import CobroContado, DetalleCobro, Factura, DetalleFactura, Caja, DetalleCaja
from gestion_administrativo.models import Persona, Paciente, PacienteTratamientoAsignado, Tratamiento
from gestion_agendamiento.models import Cita
from .forms import *
from django.db.models import Q
from datetime import datetime as class_datetime
import datetime

def mostrar_tratamientos_cobrar(request, id_paciente):
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

    caja_cerrada = False
    respuesta = verificar_apertura_caja()
    if respuesta == 'Cerrada':
        caja_cerrada = True
    else:
        caja_cerrada = False

    return render (request,"mostrar_tratamientos_cobrar.html",{
                                                        'tratamientos_agendados':tratamientos_agendados,
                                                        'persona':persona,
                                                        'precio_total':precio_total,
                                                        'menor_edad':menor_edad,
                                                        'id_paciente':id_paciente,
                                                        'caja_cerrada':caja_cerrada
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
        """ detalle_cobro_nuevo = DetalleCobroContado.objects.create(
                                                            cobro=cobro_contado,
                                                            # tratamientos=tratamientos_confirmados
        ) """
        # detalle_actualiado =DetalleCobroContado.objects.filter(cobro=cobro_contado).update()
        for tratamiento_conf in tratamientos_confirmados:
            # print("Tratamiento: ",tratamiento_conf.codigo_tratamiento)
            # DetalleCobroContado.objects.filter(cobro=cobro_contado).update(tratamientos=tratamiento_conf)
            """ detalle_cobro_tratamiento = DetalleCobroTratamiento.objects.create(
                                                detalle_cobro=detalle_cobro_nuevo,
                                                tratamiento = tratamiento_conf
            ) """
        pagar_tratamientos(numero_documento)
    
        id_cobro = cobro_contado.id_cobro_contado
    else:
        return redirect("/cobros/error_cobro/")

    return redirect("/cobros/mensaje_confirmacion_cobro/%s"%(id_cobro))


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

        """ tratamientos_confirmados = obtener_tratamientos(numero_documento)
        detalle_cobro_nuevo = DetalleCobroContado.objects.create(
                                                            cobro=cobro_contado,
                                                            # tratamientos=tratamientos_confirmados
        ) """
        # detalle_actualiado =DetalleCobroContado.objects.filter(cobro=cobro_contado).update()
        """ for tratamiento_conf in tratamientos_confirmados:
            # print("Tratamiento: ",tratamiento_conf.codigo_tratamiento)
            # DetalleCobroContado.objects.filter(cobro=cobro_contado).update(tratamientos=tratamiento_conf)
            detalle_cobro_tratamiento = DetalleCobroTratamiento.objects.create(
                                                detalle_cobro=detalle_cobro_nuevo,
                                                tratamiento = tratamiento_conf
            ) """
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
    now = class_datetime.now()
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
        return redirect("/cobros/ingresar_datos_cobro/%s" %(paciente.id_paciente))
        

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

def pagar_tratamientos(tratamientos):
    """ 
        Cambia el estado de la tabla TratamientoConfirmado
        con estado = 'Pagado'
    """
    # paciente = Paciente.objects.get(numero_documento=cedula)
    # id_paciente = paciente.id_paciente
    # listado_tratamientos_conf = TratamientoConfirmado.objects.filter(estado='Confirmado')

    for tratamiento_conf in tratamientos:
        # tratamiento = TratamientoConfirmado.objects.get()
        id_tratamiento_con = tratamiento_conf.id_tratamiento_conf
        tratamiento_pag = TratamientoConfirmado.objects.filter(id_tratamiento_conf=id_tratamiento_con).update(estado='Pagado')
        # if str(tratamiento_conf.paciente.id_paciente) == str(id_paciente):
            # id_tratamiento_con = tratamiento_conf.id_tratamiento_conf
            # tratamiento_pag = TratamientoConfirmado.objects.filter(id_tratamiento_conf=id_tratamiento_con).update(estado='Pagado')


def ver_detalle_cobro(request, id_cobro_contado):
    cobro = CobroContado.objects.get(id_cobro_contado=id_cobro_contado)
    detalles_de_cobros = DetalleCobro.objects.filter(cobro_contado=cobro)
    # id_detalle_cobro = detalle_cobro.id
    # detalle_tratamientos = DetalleCobroTratamiento.objects.all()
    tratamientos =[] 

    for detalle_cobro in detalles_de_cobros:
        # print("id Detalle parametro: ", id_detalle_cobro)
        # print("Detalle de cobro en BD: ", detalle_tratamiento.detalle_cobro.id)
        # if detalle_tratamiento.detalle_cobro.id == id_detalle_cobro:
        id_tratamiento = detalle_cobro.tratamiento.get_codigo_tratamiento()
        tratamiento = Tratamiento.objects.get(codigo_tratamiento=id_tratamiento)
        precio = '{:,}'.format(tratamiento.precio).replace(',','.')
        tratamiento_tmp = {
                            'nombre_tratamiento':tratamiento.nombre_tratamiento,
                            'precio':precio
        }
        tratamientos.append(tratamiento_tmp)
            # print("Entra en detalle de cobro")
    factura = Factura.objects.get(cobro_contado=cobro, estado='Emitido')
    monto_total = factura.total_pagar
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
        try:
            factura = Factura.objects.get(cobro_contado=cobro, estado='Emitido')
        except Factura.DoesNotExist:
            pass
        else:
            monto_total = '{:,}'.format(factura.total_pagar).replace(',','.')
            cobro_tmp = {
                        'id_cobro_contado' : cobro.id_cobro_contado,
                        'numero_documento' : factura.numero_documento,
                        'razon_social' : factura.razon_social,
                        'fecha' : factura.fecha,
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
    tratamientos_confirmados = TratamientoConfirmado.objects.filter(estado='Confirmado')
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    fecha_actual= (datetime.datetime.now().strftime('%d/%m/%Y'))
    
    listado_insumos_asig= TratamientoInsumoAsignado.objects.all()
    
    tratamientos_insumos_asignados = []
    
    precio_total = 0
    
    for tratamiento in tratamientos_confirmados:
        if str(tratamiento.get_paciente()) == str(id_paciente):
            cod_tratamiento = tratamiento.get_tratamiento()
            nuevo_tratamiento = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            nuevo_insumo= []
            insumos=[]
            for insumo_asig in listado_insumos_asig:
                if str(insumo_asig.get_tratamiento()) == str(cod_tratamiento):
                    cod_insumo = insumo_asig.get_insumo()
                    nuevo_insumo = Insumo.objects.get(codigo_insumo=cod_insumo)
                    insumos.append(nuevo_insumo)
                    # print("Tratamiento: "," ", nuevo_tratamiento.nombre_tratamiento,", INSUMO: ", nuevo_insumo.nombre_insumo)
            tratamiento_insumo_asig = {
                                        "tratamiento":nuevo_tratamiento,
                                        "insumos":insumos,
            }
            tratamientos_insumos_asignados.append(tratamiento_insumo_asig)
            # print("Listado de Tratamientos con Insumo",{'tratamientos_insumos_asignados':tratamientos_insumos_asignados })
      
            precio_total = int(precio_total) + int(nuevo_tratamiento.precio)

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

def mostrar_msj_confirmacion_cobro(request,id_cobro):
    return render(request, 'mensajes/confirmacion_de_cobro.html',{'id_cobro':id_cobro})

#--------------------- Sección de faturación -------------------------------#
def ingresar_datos_factura(request, id_cobro):
    cobro = CobroContado.objects.get(id_cobro_contado=id_cobro)
    cedula = cobro.paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    """ detalle_cobro = DetalleCobroContado.objects.get(cobro=cobro) """
    id_detalle_cobro = detalle_cobro.id
    detalle_tratamientos = DetalleCobroTratamiento.objects.all()
    tratamientos =[]

    for detalle_tratamiento in detalle_tratamientos:
        if detalle_tratamiento.detalle_cobro.id == id_detalle_cobro:
            id_tratamiento = detalle_tratamiento.tratamiento.get_codigo_tratamiento()
            tratamiento = Tratamiento.objects.get(codigo_tratamiento=id_tratamiento)
            precio_numerico = tratamiento.precio
            precio = '{:,}'.format(tratamiento.precio).replace(',','.')
            tratamiento_tmp = {
                                'nombre_tratamiento':tratamiento.nombre_tratamiento,
                                'precio':precio,
                                'precio_numerico':precio_numerico
            }
            tratamientos.append(tratamiento_tmp)

    monto_total = cobro.monto_total
    monto_total_s= '{:,}'.format(monto_total).replace(',','.')

    partes_nro_factura = generar_numero_factura()

    factura = Factura(
                        sub_nro_factura1 = partes_nro_factura['sub_nro_1'],
                        sub_nro_factura2 = partes_nro_factura['sub_nro_2'],
                        sub_nro_factura3 = partes_nro_factura['sub_nro_3'],
                        nro_factura = partes_nro_factura['nro_factura'],
                        numero_documento = cobro.numero_documento,
                        razon_social = cobro.razon_social,
                        direccion = persona.direccion,
                        telefono = persona.telefono,
                        total_pagar = monto_total,
                        # iva_5 = "",
                        iva_10= (monto_total / 11),
                        total_iva = (monto_total / 11),
                        estado = 'Emitido',
    )

    data = {
        'form': FacturaForm(instance=factura)
    }

    data['tratamientos'] = tratamientos
    data['monto_total'] = monto_total_s
    data['id_factura'] = factura.id_factura

    if request.method == 'POST':
        # form = CobroFacturaForm(data=request.POST, files=request.FILES, instance=cobro)
        # form2 = DatosFacturaForm(data=request.POST, files=request.FILES, instance=persona)
        form = FacturaForm(data=request.POST, files=request.FILES, instance=factura)

        if form.is_valid():
            form.save()
            fact = Factura.objects.last()
            id_factura = fact.id_factura
            guardar_detalle_factura(fact, tratamientos)
            return redirect("/cobros/generar_factura/%s" %(id_factura))
        else:
            data['form']=form
    else:
        print("No entra en POST")

    return render(request, 'facturacion/ingresar_datos_factura.html', data)


def generar_numero_factura():
    try:
        factura = Factura.objects.last()
    except Factura.DoesNotExist: 
        sub_nro_1 = '001'
        sub_nro_2 = '001'
        sub_nro_3 = 1
        digitos = len(str(sub_nro_3))
        nro_factura = sub_nro_1 +"-"+sub_nro_2+"-"
        cantidad_max = 7
        cant_digitos = digitos
        while(cant_digitos < cantidad_max):
            nro_factura = nro_factura +"0"
            cant_digitos = cant_digitos + 1
        nro_factura = nro_factura + str(sub_nro_3 + 1)

        partes_nro_factura = {
                        'sub_nro_1' : sub_nro_1,
                        'sub_nro_2' : sub_nro_2,
                        'sub_nro_3' : (sub_nro_3+1),
                        'nro_factura' : nro_factura,
        }

        return partes_nro_factura
    else:
        sub_nro_1 = factura.sub_nro_factura1
        sub_nro_2 = factura.sub_nro_factura2
        sub_nro_3 = factura.sub_nro_factura3
        nro_factura = sub_nro_1 +"-"+sub_nro_2+"-"

        digitos = len(str(sub_nro_3))
        cantidad_max = 7
        cant_digitos = digitos
        while(cant_digitos < cantidad_max):
            nro_factura = nro_factura +"0"
            cant_digitos = cant_digitos + 1
        nro_factura = nro_factura + str(sub_nro_3 + 1)

        partes_nro_factura = {
                            'sub_nro_1' : sub_nro_1,
                            'sub_nro_2' : sub_nro_2,
                            'sub_nro_3' : (sub_nro_3+1),
                            'nro_factura' : nro_factura,
        }
        print('partes_nro_factura: ',partes_nro_factura)
        return partes_nro_factura


def guardar_detalle_factura(fact, tratamientos):
    print("Entra a guardar detalle de factura")
    for t in tratamientos:
        detalle_factura = DetalleFactura.objects.create(
                                                    id_factura = fact,
                                                    descripcion = t.tratamiento.nombre_tratamiento,
                                                    precio_unitario = t.tratamiento.precio,
                                                    gravado_10_porc = t.tratamiento.precio,
        )


def visualizar_datos_factura(request, id_factura):
    factura = Factura.objects.get(id_factura=id_factura)
    fecha = factura.fecha

    data={
        'form':FacturaReadOnlyForm(instance=factura),
        'fecha':fecha
    }

    if request.method == 'POST':
        form = FacturaReadOnlyForm(data=request.POST, instance=factura, files=request.FILES)

    return render(request, 'facturacion/visualizar_datos_factura.html', data)


#--->Factura HTML----
def generar_factura_original(request):
    return render(request, 'modelos_factura/generar_factura_original.html')

#--->Factura PDF----
def generar_factura(request,id_factura):
    #--Empresa--#
    empresa= Empresa.objects.last()
    factura = Factura.objects.get(id_factura=id_factura)
    detalle_factura = DetalleFactura.objects.filter(id_factura=id_factura)
  
    
    data = {
        'empresa': empresa,
        'factura':factura,
        'detalle_factura': detalle_factura
    }

  
    pdf = render_to_pdf("generar_factura.html",data)
    
    return HttpResponse(pdf, content_type='application/pdf')


#--->Listado de Facturas----#
def listar_facturas (request):
    facturas = Factura.objects.all().order_by('nro_factura')
    lista_facturas = []
    anulado = False
    for factura in facturas:
        if factura.estado == 'Anulado':
            anulado = True
        else:
            anulado = False
        dato_factura = {
                        'factura': factura,
                        'anulado': anulado
        }
        print('Anulado?: ', anulado)
        lista_facturas.append(dato_factura)
    return render(request, 'listar_facturas.html', {'lista_facturas':lista_facturas})

def cambiar_estado_factura(request, id_factura):
    factura = Factura.objects.get(id_factura=id_factura)
    fecha = factura.fecha
    print('nro de factura: ', factura.id_factura)

    data={
        'form':FacturaUpdateForm(instance=factura),
        'fecha':fecha
    }

    if request.method == 'POST':
        form = FacturaUpdateForm(data=request.POST, instance=factura, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Estado cambiado correctamente✅')
            return redirect('/cobros/listar_facturas/')
        else:
            data['form']=form
            data['fecha']=fecha

    return render(request, 'facturacion/cambiar_estado_factura.html', data)


def verificar_apertura_caja ():
    now = class_datetime.now()
    fecha_actual = now.date()
    try:
        caja = Caja.objects.get(fecha_apertura=fecha_actual)
    except Caja.DoesNotExist:
        respuesta = 'Cerrada'
        return respuesta
    
    respuesta = 'Abierta'

    return respuesta


def mostrar_caja(request, numero_documento):
    data = {
            'numero_documento':numero_documento,
    }
    respuesta = verificar_apertura_caja()
    if respuesta == "Cerrada":
        return render(request, 'mensajes/msj_caja_cerrada2.html', data)

    return render(request, 'mensajes/msj_caja_abierta2.html')


def mostrar_msj_caja_cerrada(request, numero_documento):
    data = {
            'numero_documento':numero_documento,
    }
    respuesta = verificar_apertura_caja()
    if respuesta == "Cerrada":
        return render(request, 'mensajes/msj_caja_cerrada.html', data)

    return render(request, 'mostrar_caja.html')



def guardar_datos_apertura_caja(request, numero_documento, id_paciente):
    cajero = Funcionario.objects.get(numero_documento=numero_documento)
    now = class_datetime.now()
    fecha_actual = now.date()
    hora_actual = now.time()

    total_caja  = CobroContado.objects.all().aggregate(Sum('monto_total'))

    caja_temp = Caja(
                    id_cajero = cajero,
                    fecha_apertura = fecha_actual,
                    hora_apertura = hora_actual,
                    # saldo_anterior = total_caja['monto_total__sum'],
    )

    monto_total_s= '{:,}'.format(total_caja['monto_total__sum']).replace(',','.')

    data = {
            'form':CajaForm(instance=caja_temp),
            'fecha_actual':fecha_actual,
            'hora_actual':hora_actual,
            'saldo_anterior':monto_total_s,
    }

    data2 = {
        'id_paciente':id_paciente
    }

    if request.method == 'POST':
        form = CajaForm(data = request.POST, files=request.FILES)
        if form.is_valid():
            caja = form.save(commit=False)
            caja.id_cajero = cajero
            caja.fecha_apertura = fecha_actual
            caja.hora_apertura = hora_actual
            caja.save()
            return render(request, 'mensajes/msj_caja_abierta.html', data2)
        else:
            print('form no es valido')
            data['form'] = CajaForm
            data['fecha_actual'] = fecha_actual
            data['hora_actual'] = hora_actual
    return render(request, 'guardar_datos_apertura_caja.html', data)


def guardar_datos_apertura_caja2(request, numero_documento):
    cajero = Funcionario.objects.get(numero_documento=numero_documento)
    now = class_datetime.now()
    fecha_actual = now.date()
    hora_actual = now.time()

    total_caja  = CobroContado.objects.all().aggregate(Sum('monto_total'))

    caja_temp = Caja(
                    id_cajero = cajero,
                    fecha_apertura = fecha_actual,
                    hora_apertura = hora_actual,
                    # saldo_anterior = total_caja['monto_total__sum'],
    )

    monto_total_s= '{:,}'.format(total_caja['monto_total__sum']).replace(',','.')

    data = {
            'form':CajaForm(instance=caja_temp),
            'fecha_actual':fecha_actual,
            'hora_actual':hora_actual,
            'saldo_anterior':monto_total_s,
    }

    if request.method == 'POST':
        form = CajaForm(data = request.POST, files=request.FILES)
        if form.is_valid():
            caja = form.save(commit=False)
            caja.id_cajero = cajero
            caja.fecha_apertura = fecha_actual
            caja.hora_apertura = hora_actual
            caja.save()
            return render(request, 'mensajes/msj_caja_abierta2.html')
        else:
            print('form no es valido')
            data['form'] = CajaForm
            data['fecha_actual'] = fecha_actual
            data['hora_actual'] = hora_actual
    return render(request, 'guardar_datos_apertura_caja.html', data)

3

def msj_caja_cerrada(request, id_paciente, numero_documento):
    data = {
            'numero_documento':numero_documento,
            'id_paciente':id_paciente,
    }
    return render(request, 'mensajes/msj_caja_cerrada.html', data)

def msj_caja_abierta2(request):
    return render(request, ',mensajes/msj_caja_abierta2.html')

def ingresar_datos_cobro(request, id_paciente):
    paciente = Paciente.objects.get(id_paciente=id_paciente)

    tratamientos = TratamientoConfirmado.objects.filter(
                                                        paciente = id_paciente,
                                                        estado = 'Confirmado'
    )

    for t in tratamientos:
        monto_total = t.tratamiento.precio

    monto_total_s= '{:,}'.format(monto_total).replace(',','.')
    now = class_datetime.now()
    fecha_actual = now.date()

    partes_nro_factura = generar_numero_factura()
    factura = Factura(
                        sub_nro_factura1 = partes_nro_factura['sub_nro_1'],
                        sub_nro_factura2 = partes_nro_factura['sub_nro_2'],
                        sub_nro_factura3 = partes_nro_factura['sub_nro_3'],
                        nro_factura = partes_nro_factura['nro_factura'],
                        numero_documento = paciente.numero_documento,
                        razon_social = paciente.numero_documento.nombre +" "+ paciente.numero_documento.apellido,
                        direccion = paciente.numero_documento.direccion,
                        telefono = paciente.numero_documento.telefono,
                        fecha = fecha_actual,
                        total_pagar = monto_total,
                        # iva_5 = "",
                        iva_10= (monto_total / 11),
                        total_iva = (monto_total / 11),
                        estado = 'Emitido',
    )

    data = {
            'tratamientos':tratamientos,
            'monto_total':monto_total_s,
            # 'fecha':fecha_actual,
            'form': FacturaForm(instance=factura)
    }

    if request.method == 'POST':
        form = FacturaForm(data=request.POST, files=request.FILES, instance=factura)

        if form.is_valid():
            cobro = CobroContado.objects.create(
                                                paciente=paciente 
            )

            for t in tratamientos:
                detalle_cobro = DetalleCobro.objects.create(
                                                    tratamiento=t.tratamiento,
                                                    cobro_contado=cobro
                )
            factura = form.save(commit=False)
            factura.cobro_contado = cobro
            factura.save()
            fact = Factura.objects.last()
            # id_factura = fact.id_factura
            guardar_detalle_factura(fact, tratamientos)
            guardar_detalle_caja(fact, tratamientos)
            pagar_tratamientos(tratamientos)
            return redirect('/cobros/confirmacion_de_cobro/%s' %(fact.id_factura))

    return render(request, 'ingresar_datos_cobro.html', data)


def confirmacion_de_cobro(request, id_factura):
    return render(request, 'mensajes/confirmacion_de_cobro.html', {'id_factura':id_factura})


def guardar_detalle_caja(factura, tratamientos):
    now = class_datetime.now()
    fecha_actual = now.date()
    caja = Caja.objects.get(fecha_apertura=fecha_actual)

    for t in tratamientos:
        detalle_caja = DetalleCaja.objects.create(
                                            id_caja = caja,
                                            detalle = t.tratamiento.nombre_tratamiento,
                                            comprobante_cobro = factura
        )

def cerrar_caja(request):
    now = class_datetime.now()
    fecha_actual = now.date()
    hora_actual = now.time()
    caja = Caja.objects.get(fecha_apertura=fecha_actual)

    detalles_cajas = DetalleCaja.objects.filter(id_caja=caja.id_caja)
    monto_total = 0

    for detalle_caja in detalles_cajas:
        factura = Factura.objects.get(id_factura=detalle_caja.comprobante_cobro)
        monto_total = monto_total + factura.total_pagar

    caja.update(
                monto_cierre=monto_total,
                fecha_cierre=fecha_actual,
                hora_cierre=hora_actual
    )

#---------------------- Gastos ----------------------------------#
def registrar_gasto(request):
    now = class_datetime.now()
    fecha_actual = now.date()
    data = {
            'form':ComprobanteGastoForm(),
            # 'form2':DetalleComprobanteForm(),
            # 'fecha_actual':fecha_actual
    }
    if request.method == 'POST':
        form = ComprobanteGastoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            combrobante_gasto = ComprobanteGasto.objects.last()
            return redirect('/cobros/agregar_detalle_comprobante/%s'%(combrobante_gasto.id_comprobante))
        else:
            print("Form no es valido")
            data['form'] = ComprobanteGastoForm()
    return render(request, 'gastos/registrar_gasto.html', data)


def agregar_detalle_comprobante(request, id_comprobante):
    comprobante_gasto = ComprobanteGasto.objects.get(id_comprobante=id_comprobante)
    data = {
            'form':DetalleComprobanteForm(),
            'form2':ComprobanteReadOnly(instance=comprobante_gasto),
            'id_comprobante':id_comprobante,
    }
    try:
        detalles = DetalleComprobante.objects.filter(comprobante=id_comprobante)
    except DetalleComprobante.DoesNotExist:
        pass
    else:
        data['detalles'] = detalles

    if request.method == 'POST':
        form = DetalleComprobanteForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.comprobante = comprobante_gasto
            detalle.save()
            return redirect('/cobros/agregar_detalle_comprobante/%s'%(comprobante_gasto.id_comprobante))
    return render(request, 'gastos/agregar_detalle_comprobante.html', data)


def agregar_monto_total(request, id_comprobante):
    comprobante = ComprobanteGasto.objects.get(id_comprobante=id_comprobante)
    suma_detalles = DetalleComprobante.objects.filter(comprobante=id_comprobante).aggregate(Sum('precio_unitario'))
    iva_5_detalles = DetalleComprobante.objects.filter(comprobante=id_comprobante).aggregate(Sum('iva_5'))
    iva_10_detalles = DetalleComprobante.objects.filter(comprobante=id_comprobante).aggregate(Sum('iva_10'))
    monto_total = suma_detalles['precio_unitario__sum']
    d_iva_5 = iva_5_detalles['iva_5__sum']
    d_iva_10 = iva_10_detalles['iva_10__sum']
    
    comprobante_tmp = ComprobanteGasto(
                                    id_comprobante = comprobante.id_comprobante,
                                    razon_social = comprobante.razon_social,
                                    numero_comprobante = comprobante.numero_comprobante,
                                    timbrado = comprobante.timbrado,
                                    condicion_venta = comprobante.condicion_venta,
                                    total_iva_5 = d_iva_5,
                                    total_iva_10 = d_iva_10,
                                    monto_total = monto_total,
                                    fecha = comprobante.fecha,
    )

    data = {
            'form2':ComprobanteReadOnly(instance=comprobante),
            'form':ComprobanteMontoForm(instance=comprobante_tmp)
    }

    try:
        detalles = DetalleComprobante.objects.filter(comprobante=id_comprobante)
    except DetalleComprobante.DoesNotExist:
        pass
    else:
        data['detalles'] = detalles

    if request.method == 'POST':
        form = ComprobanteMontoForm(data=request.POST, files=request.FILES, instance=comprobante_tmp)
        if form.is_valid():
            form.save()
            registrar_gasto_en_caja(id_comprobante)
            return redirect('/cobros/listar_gastos/')
    return render(request, 'gastos/agregar_monto_total.html', data)


def listar_gastos(request):
    gastos = ComprobanteGasto.objects.all()
    data = {
            'gastos':gastos
    }
    return render(request, 'gastos/listar_gastos.html', data)


def registrar_gasto_en_caja(id_comprobante):
    caja = Caja.objects.last()
    comprobante = ComprobanteGasto.objects.get(id_comprobante=id_comprobante)
    detalle_caja = DetalleCaja.objects.create(
                                            id_caja = caja,
                                            tipo = 'Egreso',
                                            comprobante_pago = comprobante,
    )

