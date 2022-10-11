from genericpath import exists
from mailbox import NoSuchMailboxError
from operator import truediv
from re import U
from time import gmtime, strftime, strptime
from urllib import request
from django.utils.html import conditional_escape as esc
from itertools import groupby
from datetime import date, timedelta
from calendar import HTMLCalendar, day_name
from ctypes.wintypes import PCHAR
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from gestion_administrativo.forms import PersonaPacienteForm
from gestion_administrativo.forms import PersonaUpdateForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from webapp.mixins import LoginMixin
from django.db.models import Q
from .forms import *
# Create your views here.
from django.contrib import messages
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,)
from django.contrib.auth.decorators import permission_required
# ---------Vista Principal-------
from datetime import datetime
import calendar
import datetime
# import locale
# locale.setlocale(locale.LC_ALL,"es_py.UTF-8")

# print(datetime.today().weekday())
# curr_date = date.today()
# print(calendar.day_name[curr_date.weekday()])
# #print(list(calendar.day_name))

# then = datetime(1987, 12, 30, 17, 50, 14)  # yr, mo, day, hr, min, sec
# now = datetime(2020, 12, 25, 23, 13, 0)
# print(then-now)

#Funcion que trae el dia de la fecha de la Semana

def dia_semana(date): 
    born = datetime.datetime.strptime(date, '%d/%m/%Y').weekday() 
    # hora_actual = datetime.strftime('%d/%m/%Y %H:%M:%S')
    # print("Hora actual", hora_actual)
    return (calendar.day_name[born]) 
  
date = '08/09/2022'
print(dia_semana(date))


class Calendario(LoginMixin, ListView):
    model = Cita
    template_name = 'calendar.html'
    
    # si no esta confirmado no aparece en el calendario
    # def get_queryset(self):
    #     queryset = self.model.objects.filter(
    #         estado=True)
    #     return queryset

# def calendario_vista(request):
#     return render(request, "calendario.html")
# def pruebacalendar(request):
#     return render(request, "calendar.html")


# <--Agregar cita-->|A nivel SISTEMA

def agregar_cita(request, id_paciente):
    try:
        paciente = Paciente.objects.get(id_paciente=id_paciente)
        cedula = paciente.numero_documento
        persona = Persona.objects.get(numero_documento=cedula)
        nombre = persona.nombre + ' ' + persona.apellido
        ci_persona= persona.numero_documento
        usuario=Usuario.objects.get(numero_documento=ci_persona)
        nro_telefonico = persona.telefono
        edad = persona.obtener_edad()


        cita = Cita.objects.all()
        # pk_cita=cita.id_cita
        print(nro_telefonico, nombre, "este es el año------------------",edad)
        data = {
            'form': CitaForm(),
            'persona': persona,
            # 'nro_telefonico': nro_telefonico,
            # 'pk_cita' : pk_cita

        }

        if request.method == "POST":
            formulario = CitaForm(data=request.POST, files=request.FILES)
            respuesta= "NO EXISTE"
            
            if formulario.is_valid():
                cita = formulario.save(commit=False)
                cita.paciente = paciente
                cita.nombre_paciente = nombre
                # cita.celular = nro_telefonico
                # cita.id_cita=pk_cita   
                citas= Cita.objects.all()     
            
                for c in citas:
                    dia=str (cita.fecha)
                    nro_semana = datetime.datetime.strptime(dia,'%Y-%m-%d').weekday()
                    dia = calendar.day_name[nro_semana]
                    print('es el dia', dia, "el numero de la semana  es", nro_semana)
                    ########################
                            #||DATOS|||
                    #""" 'Fecha actual' """
                    actual = datetime.datetime.now().strftime("%Y-%m-%d")
                    #""" 'Fecha que recibe' """
                    dia_recibido = str(cita.fecha)
                    #""" 'Hora actual' """
                    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                    # Imprime la Hora y la fecha actual -> actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #print("es la hora actual",hora_actual)
                    #""" 'Hora que recibe' """
                    hora_recibida = str(cita.hora_atencion)
                    ########################
                    if edad > 4:
                        if dia_recibido > actual or hora_recibida > hora_actual:
                            #        
                            #''Dias de la semana 5 y 6 es Sabado y Domingo''
                            if nro_semana <= 4:                 
                                if cita.hora_atencion == c.hora_atencion and cita.fecha==c.fecha and cita.profesional==c.profesional:
                                        #print("el numero de la semana  es", nro_semana)
                                        respuesta = "YA EXISTE"
                                        return render(request, 'horario_reservado.html')
                                else: 
                                    # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos
                                    if paciente== c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha==c.fecha:
                                            respuesta = "Reservado"
                                            # mensaje = "DUPLICADO"
                                            messages.success(request, (
                                                    'Reservado en el mismo dia y la misma hora, pero con diferentes Odontólogos'))
                                            return render(request, 'horario_duplicado.html')
                            else:
                                if nro_semana >=5: 
                                    #"Si es fin de semana emite el msj"
                                    messages.success(request, "Por favor, elija dias entre Lunes a Viernes")
                                    return render(request, 'cerrado.html')   
                        else:
                            if dia_recibido < actual or hora_recibida < hora_actual:
                                print("pasa por aqui primero||||||||||------------------")
                                respuesta = "PASADO"
                                messages.success(request, "Por favor verifique nuevamente")
                                return render(request, 'fecha_pasada.html')
                    else:
                        return render(request, 'atencion.html')

                if respuesta== "NO EXISTE":
                    
                        cita.paciente = paciente
                        cita.nombre_paciente = nombre
                        print("|||||||||||||CITA GUARDADA DEL PACIENTE QUE TIENE USUARIO||||||||||------------------")
                        # cita.celular = nro_telefonico
                        
                        cita.save()
                        messages.success(request, ('✅Agregado correctamente!'))
                        print('aquiiiiiiiiiiiiii ENTRAAAAA',)
                        return redirect("/agendamiento/listado_citas/")
                 
            else:
                messages.error(request, ('La cita no ha sido registrada'))
                data["form"] = formulario
                print('NO ENTRAAAAA')
        return render(request, "agregar_cita.html", data)
    
    except Usuario.DoesNotExist:
    #   messages.error(request, " ⚠ Esta persona no cuenta con un usuario propio")
    # return render(request, "autorizar_modificacion.html")
        return redirect("/agendamiento/agregar_cita_usuario/%s" %(id_paciente))


def agendar_cita(request, id_paciente, codigo_tratamiento):
    """
    Esta función permite al Asistente agendarle una cita a un paciente sobre 
    un tratamiento que el Odontologo le haya asignado
    """
    tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    nombre = persona.nombre + ' ' + persona.apellido
    # ci_persona= persona.numero_documento
    # usuario=Usuario.objects.get(numero_documento=ci_persona)
    nro_telefonico = persona.telefono
    edad = persona.obtener_edad()


    cita = Cita.objects.all()
    # pk_cita=cita.id_cita
    print(nro_telefonico, nombre, "este es el año------------------",edad)
    data = {
        'form': CitaForm2(),
        'persona': persona,
        'tratamiento':tratamiento,
        }

    if request.method == "POST":
        formulario = CitaForm2(data=request.POST, files=request.FILES)
        respuesta= "NO EXISTE"

        if formulario.is_valid():
            cita = formulario.save(commit=False)
            cita.paciente = paciente
            cita.nombre_paciente = nombre
            cita.tratamiento_solicitado = tratamiento
            citas= Cita.objects.all()     

            for c in citas:
                dia=str (cita.fecha)
                nro_semana = datetime.datetime.strptime(dia,'%Y-%m-%d').weekday()
                dia = calendar.day_name[nro_semana]
                print('es el dia', dia, "el numero de la semana  es", nro_semana)
                ########################
                        #||DATOS|||
                #""" 'Fecha actual' """
                actual = datetime.datetime.now().strftime("%Y-%m-%d")
                #""" 'Fecha que recibe' """
                dia_recibido = str(cita.fecha)
                #""" 'Hora actual' """
                hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                # Imprime la Hora y la fecha actual -> actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #print("es la hora actual",hora_actual)
                #""" 'Hora que recibe' """
                hora_recibida = str(cita.hora_atencion)
                ########################
                if edad > 4:
                    if dia_recibido > actual or hora_recibida > hora_actual:
                        #        
                        #''Dias de la semana 5 y 6 es Sabado y Domingo''
                        if nro_semana <= 4:                 
                            if cita.hora_atencion == c.hora_atencion and cita.fecha==c.fecha and cita.profesional==c.profesional:
                                    #print("el numero de la semana  es", nro_semana)
                                respuesta = "YA EXISTE"
                                return render(request, 'horario_reservado.html')
                            else: 
                                # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos
                                if paciente== c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha==c.fecha:
                                    respuesta = "Reservado"
                                    # mensaje = "DUPLICADO"
                                    messages.success(request, (
                                                    'Reservado en el mismo dia y la misma hora, pero con diferentes Odontólogos'))
                                    return render(request, 'horario_duplicado.html')
                        else:
                            if nro_semana >=5: 
                                #"Si es fin de semana emite el msj"
                                messages.success(request, "Por favor, elija dias entre Lunes a Viernes")
                                return render(request, 'cerrado.html')   
                    else:
                        if dia_recibido < actual or hora_recibida < hora_actual:
                            print("pasa por aqui primero||||||||||------------------")
                            respuesta = "PASADO"
                            messages.success(request, "Por favor verifique nuevamente")
                            return render(request, 'fecha_pasada.html')
                else:
                    return render(request, 'atencion.html')

            if respuesta== "NO EXISTE":
                cita.paciente = paciente
                cita.nombre_paciente = nombre
                print("|||||||||||||CITA GUARDADA DEL PACIENTE QUE TIENE USUARIO||||||||||------------------")
                # cita.celular = nro_telefonico

                cita.save()
                agendar_tratamiento_asignado(id_paciente, codigo_tratamiento)
                if cita.estado == True:
                    pass
                messages.success(request, ('✅Agregado correctamente!'))
                print('aquiiiiiiiiiiiiii ENTRAAAAA',)
                return redirect("/agendamiento/listado_citas/")
        else:
            messages.error(request, ('La cita no ha sido registrada'))
            data["form"] = formulario
            print('NO ENTRAAAAA')
    return render(request, "agendar_cita.html", data)


# <--Agregar cita de un MENOR DE EDAD-->|A nivel SISTEMA
def addcita_cita_usuario(request, id_paciente):
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    nombre = persona.nombre + ' ' + persona.apellido
    nro_telefonico = persona.telefono
    edad = persona.obtener_edad()

    fecha = Cita.objects.all()
    # apellido = persona.apellido

    hora_atencion = Horario.objects.all()
    # hora= HoraForm(request.POST)

    data = {
        'form': CitaForm(),
        'persona': persona,
        'id_paciente': id_paciente,
        'hora_atencion': hora_atencion,
        # 'celular':celular,
    }

    if request.method == "POST":
        formulario = CitaForm(data=request.POST, files=request.FILES)
        respuesta = "NO EXISTE"

        if formulario.is_valid():
            cita = formulario.save(commit=False)
            citas = Cita.objects.all()
            for c in citas:
                #dia= cita.fecha
                dia = str(cita.fecha)
                nro_semana = datetime.datetime.strptime(
                    dia, '%Y-%m-%d').weekday()
                dia = calendar.day_name[nro_semana]
               ########################
                #||DATOS|||
                #""" 'Fecha actual' """
                actual = datetime.datetime.now().strftime("%Y-%m-%d")
                #""" 'Fecha que recibe' """
                dia_recibido = str(cita.fecha)
                #""" 'Hora actual' """
                hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                # Imprime la Hora y la fecha actual -> actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #print("es la hora actual",hora_actual)
                #""" 'Hora que recibe' """
                hora_recibida = str(cita.hora_atencion)
                ########################
                if edad > 4:
                    if dia_recibido > actual or hora_recibida > hora_actual:
                        #
                        #''Dias de la semana 5 y 6 es Sabado y Domingo''
                        if nro_semana <= 4:
                            if cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional:
                                #print("el numero de la semana  es", nro_semana)
                                respuesta = "YA EXISTE"
                                return render(request, 'horario_reservado.html')
                            else:
                                # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos
                                if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha:
                                    respuesta = "Reservado"
                                    # mensaje = "DUPLICADO"
                                    messages.success(request, (
                                        'Reservado en el mismo dia y la misma hora, pero con diferentes Odontólogos'))
                                    return render(request, 'horario_duplicado.html')
                        else:
                            if nro_semana >= 5:
                                #"Si es fin de semana emite el msj"
                                messages.success(
                                    request, "Por favor, elija dias entre Lunes a Viernes")
                                return render(request, 'cerrado.html')
                    else:
                        if dia_recibido < actual or hora_recibida < hora_actual:
                            print(
                                "pasa por aqui primero||||||||||------------------")
                            respuesta = "PASADO"
                            messages.success(
                                request, "Por favor verifique nuevamente")
                            return render(request, 'fecha_pasada.html')
                else:
                    return render(request, 'atencion.html')

            if respuesta == "NO EXISTE":
                cita.paciente = paciente
                cita.nombre_paciente = nombre
                # cita.celular= celular
                cita.save()
                print("|||||||||||||PACIENTE QUE NO TIENE USUARIO||||||||||------------------")
                messages.success(request, (
                    '✅ Su cita ha sido registrada'))
                return render(request, "calendario.html")
        else:
            messages.error(request, (
                'No ha guardado'))
            data["form"] = formulario
            print('NO ENTRAAAAA')

    return render(request, "agregar_cita_usuario.html", data)

# <--Agregar cita a UN USUARIO--->|A nivel USUARIO
#<--Cualquier usuario
def addcita_usuario(request, numero_documento):
    persona = Persona.objects.get(numero_documento=numero_documento)
    # cedula = persona.numero_documento
    paciente = Paciente.objects.get(numero_documento=numero_documento)
    id_paciente = paciente.id_paciente
    nombre = persona.nombre + ' ' + persona.apellido
    
    # celular= persona.telefono
    # print(celular, nombre,"este es ------------------")
    
    # cita=Cita.objects.all()
    # reservado= cita.estado
    
    # apellido = persona.apellido
    print('Esta es la cedula: ', numero_documento, 'Este es el id del paciente: ', id_paciente) 
   
    hora_atencion= Horario.objects.all()
    # hora= HoraForm(request.POST)
    
    data = {
        'form': CitaForm(),
        'persona': persona,
        'id_paciente': id_paciente,
        'hora_atencion': hora_atencion,
        # 'celular':celular,
      
    }

    if request.method == "POST":
        formulario = CitaForm(data=request.POST, files=request.FILES)
        respuesta= "NO EXISTE"
    
        if formulario.is_valid():
            cita = formulario.save(commit=False)
            citas= Cita.objects.all()
            
            for c in citas:
                #dia= cita.fecha
                # Dato que arroja 6meses despues de la fecha que ha ingresado ->fecha_meses= str((cita.fecha)+ timedelta(365/2))
              #  anhio= fecha_meses.year -1
                # print('es la fecha', fecha_meses)
                dia=str (cita.fecha)
                nro_semana = datetime.datetime.strptime(dia,'%Y-%m-%d').weekday()
                dia = calendar.day_name[nro_semana]
                print('es el dia', dia, "el numero de la semana  es", nro_semana)
               ########################
                      #||DATOS|||
                #""" 'Fecha actual' """
                actual = datetime.datetime.now().strftime("%Y-%m-%d")
                #print('es la fecha', actual)
                #"""Seis meses despues de la fecha actual"
                fecha_meses = (datetime.date.today() )+ timedelta(365/2)
                print('es la Fecha DENTRO DE 6MESES', fecha_meses)
                #""" 'Fecha que recibe' """
                dia_recibido = str(cita.fecha)
                #""" 'Hora actual' """
                hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                # Imprime la Hora y la fecha actual -> actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #print("es la hora actual",hora_actual)
                #""" 'Hora que recibe' """
                hora_recibida = str(cita.hora_atencion)
                ########################
                if str(fecha_meses) > dia_recibido:
                   
                    if dia_recibido > actual or hora_recibida > hora_actual:
                        #        
                        #''Dias de la semana 5 y 6 es Sabado y Domingo''
                        if nro_semana <= 4:  
                            print("-----------------------------Nivel Sistema----------------------")                 
                            if cita.hora_atencion == c.hora_atencion and cita.fecha==c.fecha and cita.profesional==c.profesional:
                                    #print("el numero de la semana  es", nro_semana)
                                    respuesta = "YA EXISTE"
                                    return render(request, 'horario_reservado.html')
                            else: 
                                # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos
                                if paciente== c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha==c.fecha:
                                        respuesta = "Reservado"
                                        # mensaje = "DUPLICADO"
                                        messages.success(request, (
                                                'Reservado en el mismo dia y la misma hora, pero con diferentes Odontólogos'))
                                        return render(request, 'horario_duplicado.html')
                        else:
                            if nro_semana >=5: 
                                #"Si es fin de semana emite el msj"
                                messages.success(request, "Por favor, elija dias entre Lunes a Viernes")
                                return render(request, 'cerrado.html')   
                    else:
                        if dia_recibido < actual or hora_recibida < hora_actual:
                            print("pasa por aqui primero||||||||||------------------")
                            respuesta = "PASADO"
                            messages.success(request, "Por favor verifique nuevamente")
                            return render(request, 'fecha_pasada.html')
                else:
                    if str(fecha_meses) < dia_recibido:
                #     # dia_recibido se toma la fecha que ingresa por lo tanto, aca el dia que recibe sera mayor que dentro de 6meses, y fecha_meses sera
                #     #menor a lo que recibe porque se cuenta desde la fecha actual y no desde la fecha que se ingresa
                #     # print("---imprime feha en seis meses", anhio)
                        return render(request, 'atencion_fecha.html')  
              
                        
            if respuesta== "NO EXISTE" :
                cita.paciente = paciente
                cita.nombre_paciente = nombre 
                # cita.estado= reservado
                cita.save()
                print("###Guarda la CITA  DEL USUARIO REGISTRADO-----------------",cita.estado,"dentro de 6meses" ,fecha_meses, "fecha de CITA", cita.fecha,)
                messages.success(request, (
                    '✅ Su cita ha sido registrada'))
                return render(request, "calendario.html")
        else:
            messages.error(request, (
                'No ha guardado'))
            data["form"] = formulario
            print('NO ENTRAAAAA')
        messages.error(request, (
                'No ha guardado la cita...........HA FALLADO'))
    return render(request, "usuario_addCita.html", data)


 # @permission_required('gestion_agendamiento.cambiarCita_usuario', login_url="/panel_control/error/",)
#->|A NIVEL USUARIO (que tiene usuario) 
def cambiarCita_usuario(request, id_cita):
    try:
        cita = Cita.objects.get(id_cita=id_cita)
        cedula = cita.paciente
        persona = Persona.objects.get(numero_documento=cedula)
        ci_persona= persona.numero_documento
        ci_user= Usuario.objects.get(numero_documento=ci_persona)
        nro_documento=ci_user.numero_documento
        persona_user=ci_user.usuario
        # user = Usuario.objects.filter(usuario=request.user.usuario)
        # cedula_user=user.usuario    
        nombre = persona.nombre + ' ' + persona.apellido
        paciente = Paciente.objects.get(numero_documento=nro_documento)
        id_paciente = paciente.id_paciente
        reservado=cita.estado

        data = {
            'form': CitaForm(instance=cita),
            'persona': persona,
            'id_cita': id_cita,
            'ci_user':ci_user,
            'nro_documento': nro_documento,
            'id_paciente': id_paciente,
            'estado': reservado,
            # 'cedula_user':cedula_user
            
        }
        if request.method == "POST":
            formulario = CitaForm(data=request.POST, instance= cita,files=request.FILES)
            respuesta= "NO EXISTE"
            reservado = cita.estado
            
            if formulario.is_valid():
                cita = formulario.save(commit=False)
                citas= Cita.objects.all()
                
                for c in citas:
                    #---Datos---#
                    dia = str(cita.fecha)
                    nro_semana = datetime.datetime.strptime(
                        dia, '%Y-%m-%d').weekday()
                    dia = calendar.day_name[nro_semana]
                    #""" 'Fecha actual' """
                    actual = datetime.datetime.now().strftime("%Y-%m-%d")
                    #""" 'Fecha que recibe' """
                    dia_recibido = str(cita.fecha)
                    #""" 'Hora actual' """
                    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                    # Imprime la Hora y la fecha actual -> actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #print("es la hora actual",hora_actual)
                    #""" 'Hora que recibe' """
                    hora_recibida = str(cita.hora_atencion)
                    #-----------#
                    if dia_recibido > actual or hora_recibida > hora_actual or c.estado == False:
                        #
                        #''Dias de la semana 5 y 6 es Sabado y Domingo''
                        if nro_semana <= 4:
                            if cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional and reservado == False:
                                #print("el numero de la semana  es", nro_semana)
                                respuesta = "YA EXISTE"
                                return render(request, 'horario_reservado.html')
                            else:
                                # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos
                                if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional and reservado == False:
                                    respuesta = "Reservado"
                                    # mensaje = "DUPLICADO"
                                    messages.success(request, (
                                        'Reservado en el mismo dia y la misma hora, pero con diferentes Odontólogos'))
                                    return render(request, 'horario_duplicado.html')
                        else:
                            if nro_semana >= 5:
                                #"Si es fin de semana emite el msj"
                                messages.success(
                                    request, "Por favor, elija dias entre Lunes a Viernes")
                                return render(request, 'cerrado.html')
                    else:
                        if dia_recibido < actual or hora_recibida < hora_actual or reservado == True:
                            print("pasa por aqui primero||||||||||------------------")
                            respuesta = "PASADO"
                            messages.success(
                                request, "Por favor verifique nuevamente")
                            return render(request, 'fecha_pasada.html')
                        
                if respuesta== "NO EXISTE":
                    cita.paciente = paciente
                    cita.nombre_paciente = nombre
                    # cita.estado= cambio_estado
                    cita.save()
                    return redirect("/agendamiento/calendario_mensaje/")
                
            else:
                    messages.error(request, ('No ha guardado'))
                    data["form"] = formulario
                    print('NO ENTRAAAAA')
    
        return render(request, "usuario_changeCita.html", data) 
    except Usuario.DoesNotExist:
       if TypeError:
           return redirect("/agendamiento/modificar_cita_usuario/%s" % (id_cita))
       else:
            return render(request, "cita_sin_usuario.html")


# <--Modificar cita-->|A nivel SISTEMA (YA FUNCIONA EL ESTADO CONFIRMADO)
def modificar_cita(request, id_cita):
    try:
        cita = Cita.objects.get(id_cita=id_cita)
        cedula = cita.paciente
        persona = Persona.objects.get(numero_documento=cedula)
        ci_persona= persona.numero_documento
        ci_user= Usuario.objects.get(numero_documento=ci_persona)
        nro_documento=ci_user.numero_documento
        paciente = Paciente.objects.get(numero_documento=nro_documento)
        nombre = persona.nombre + ' ' + persona.apellido
        reservado=cita.estado
        data = {
            'form': CitaForm(instance=cita),
            'persona': persona,
            'estado':reservado,
        }

        if request.method == "POST":
            formulario = CitaForm(data=request.POST, instance=cita, files=request.FILES)
            respuesta= "NO EXISTE"
            
            
            if formulario.is_valid():
                cita = formulario.save(commit=False)
                citas= Cita.objects.all()
                reservado=cita.estado
                for c in citas:
                    #---Datos---#
                    dia=str (cita.fecha)
                    nro_semana = datetime.datetime.strptime(dia,'%Y-%m-%d').weekday()
                    dia = calendar.day_name[nro_semana]
                    #""" 'Fecha actual' """
                    actual = datetime.datetime.now().strftime("%Y-%m-%d")
                    #""" 'Fecha que recibe' """
                    dia_recibido = str(cita.fecha)
                    #""" 'Hora actual' """
                    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                    # Imprime la Hora y la fecha actual -> actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #print("es la hora actual",hora_actual)
                    #""" 'Hora que recibe' """
                    hora_recibida = str(cita.hora_atencion)
                    #-----------#
                    c.estado= reservado
                    if dia_recibido > actual or hora_recibida > hora_actual or c.estado==False:
                        #
                        #''Dias de la semana 5 y 6 es Sabado y Domingo''
                        if nro_semana <= 4:
                            print(
                                "-----------------------------DIA DE LA SEMANA----------------------")
                            print("el estado que entra es", reservado)
                            if cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional and reservado==False:
                                #print("el numero de la semana  es", nro_semana)
                                respuesta = "YA EXISTE"
                                return render(request, 'horario_reservado.html')
                            else:
                                # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos
                                if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and reservado== False:
                                    respuesta = "Reservado"
                                    # mensaje = "DUPLICADO"
                                    messages.success(request, (
                                        'Reservado en el mismo dia y la misma hora, pero con diferentes Odontólogos'))
                                    return render(request, 'horario_duplicado.html')
                        else:
                            if nro_semana >= 5:
                                #"Si es fin de semana emite el msj"
                                messages.success(
                                    request, "Por favor, elija dias entre Lunes a Viernes")
                                return render(request, 'cerrado.html')
                    else:
                        if dia_recibido < actual or hora_recibida < hora_actual or reservado== True:
                            print("pasa por aqui primero||||||||||------------------")
                            respuesta = "PASADO"
                            messages.success(
                                request, "Por favor verifique nuevamente")
                            return render(request, 'fecha_pasada.html')

                if respuesta== "NO EXISTE":
                    cita.paciente = paciente
                    cita.nombre_paciente = nombre
                    cita.estado=reservado
                    cita.save()
                    print("el estado que GUARDA ES", cita.estado)
                    if cita.estado == True:
                        confirmar_cita_tratamiento(cita.paciente.id_paciente, cita.tratamiento_solicitado.codigo_tratamiento)
                    messages.success(request, (
                        '✅ Modificado correctamente!'))            
                    return redirect("/agendamiento/listado_citas/", respuesta)                
            else:
                messages.error(request, "Algo ha salido Mal, por favor verifique nuevamente")
        return render(request, "modificar_cita.html", data)
    except Usuario.DoesNotExist:
            # messages.error(request, " ⚠ Esta persona no cuenta con un usuario propio")
    # return render(request, "autorizar_modificacion.html")
     return redirect("/agendamiento/modificar_cita_usuario/%s" %(id_cita))
        

# <--Modificar cita DE UNA PERSONA SIN USUARIO o MENOR DE EDAD-->|A nivel SISTEMA
def modificar_cita_usuario(request, id_cita):
    # try:    
        cita = Cita.objects.get(id_cita=id_cita)
        cedula = cita.paciente
        persona = Persona.objects.get(numero_documento=cedula)
        ci_persona = persona.numero_documento
        # ci_user = Usuario.objects.get(numero_documento=ci_persona)
        nro_documento = persona.numero_documento
        paciente = Paciente.objects.get(numero_documento=nro_documento)
        nombre = persona.nombre + ' ' + persona.apellido
        reservado = cita.estado
        
        data = {
            'form': CitaForm(instance=cita),
            'persona': persona,
            'estado': reservado,
        }

        if request.method == "POST":
            formulario = CitaForm(
                data=request.POST, instance=cita, files=request.FILES)
            respuesta = "NO EXISTE"
           

            if formulario.is_valid():
                cita = formulario.save(commit=False)
                citas = Cita.objects.all()
                reservado=cita.estado
                print ("AQUI ENTRA Y SU Estado ES", reservado)
                for c in citas:
                    #---Datos---#
                    dia = str(cita.fecha)
                    nro_semana = datetime.datetime.strptime(
                        dia, '%Y-%m-%d').weekday()
                    dia = calendar.day_name[nro_semana]
                    #""" 'Fecha actual' """
                    actual = datetime.datetime.now().strftime("%Y-%m-%d")
                    #""" 'Fecha que recibe' """
                    dia_recibido = str(cita.fecha)
                    #""" 'Hora actual' """
                    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                    # Imprime la Hora y la fecha actual -> actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    #print("es la hora actual",hora_actual)
                    #""" 'Hora que recibe' """
                    hora_recibida = str(cita.hora_atencion)
                    #-----------#
                    c.estado= reservado
                    if dia_recibido > actual or hora_recibida > hora_actual  :
                        #
                        #''Dias de la semana 5 y 6 es Sabado y Domingo''
                        if nro_semana <= 4:
                            print("-----------------------------Modificacion en caso de que sea menor de edad----------------------")
                            if cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional and reservado==False:
                                print("el numero de la semana  es", nro_semana, "EL ESTADO", reservado)
                                respuesta = "YA EXISTE"
                                return render(request, 'horario_reservado.html')
                            else:
                                # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos
                                if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and reservado==False:
                                    respuesta = "Reservado"
                                    # mensaje = "DUPLICADO"
                                    messages.success(request, ('Reservado en el mismo dia y la misma hora, pero con diferentes Odontólogos'))
                                    return render(request, 'horario_duplicado.html')
                        else:
                            if nro_semana >= 5:
                                #"Si es fin de semana emite el msj"
                                messages.success(request, "Por favor, elija dias entre Lunes a Viernes")
                                return render(request, 'cerrado.html')
                    else:
                        if dia_recibido < actual or hora_recibida < hora_actual or reservado == True:
                            print("pasa por aqui primero||||||||||------------------")
                            respuesta = "PASADO"
                            messages.success(request, "Por favor verifique nuevamente")
                            return render(request, 'fecha_pasada.html')
        
                if respuesta == "NO EXISTE":
                    cita.paciente = paciente
                    cita.nombre_paciente = nombre
                    cita.estado=reservado
                    cita.save()
                    print("GUARDA||||||||||------------------")

                    messages.success(request, (
                        '✅ Modificado correctamente!'))
                    return redirect("/agendamiento/listado_citas/", respuesta)
            else:
                messages.error(request, "Algo ha salido Mal, por favor verifique nuevamente")
        return render(request, "modificar_cita_usuario.html", data)
    # except Usuario.DoesNoExist:
    #      messages.error(
    #                 request, "Algo ha salido Mal")
        

# <--Eliminar cita-->
def eliminar_cita(request, id_cita):
    try:
        citas = Cita.objects.get(id_cita=id_cita)
        citas.delete()
        # listado_citas = Cita.objects.all()

        messages.success(request, "❌ Cita Eliminada")

        return redirect( "/agendamiento/listado_citas/")

    except Cita.DoesNotExist:
        raise Http404(
            "No se puede eliminar la cita indicada. Dado que ya se Eliminó")
        
#Eliminar la cita de un usuario(hecho)
def deletecita(request,id_cita):
    try:
       
        cita = Cita.objects.get(id_cita=id_cita)
        cedula = cita.paciente
        persona = Persona.objects.get(numero_documento=cedula)
        ci = persona.numero_documento
        ci_user = Usuario.objects.get(numero_documento=ci)
        # if (ci_user == cedula):
        cita.delete()       
        return render(request, "delete_cita.html")
        # else:
        #     messages.info(request, "⚠️Lamentamos informarle que NO puede eliminar otra cita que no sea la suya")
        #     return render(request, "panel_control/error.html")  
    except Cita.DoesNotExist:
        raise Http404(
            "No se puede eliminar la cita indicada. Dado que ya se Elimino")


# <--listado de los pacientes para agendar una cita
def listar_citapaciente(request):
    busqueda = request.POST.get("q")
    paciente_cita = Paciente.objects.all()

    if busqueda:

        # paciente_cita = Paciente.objects.filter(
        #     numero_documento__in=[busqueda])
        paciente_cita = Paciente.objects.filter(
        numero_documento__in=[busqueda])
        # queryset = queryset.filter(nombre__contains=Q, apellido__contains=Q)
        # print("AQUI ESTA ENTRANDO", queryset)

    return render(request, "pacientes_cita.html", {
        'paciente_cita': paciente_cita})

# <-Listar cita AGENDADA-->
def listar_cita(request):
    busqueda = request.POST.get("q")
      #'filtro de fecha, y nombre 
    filtro = request.POST.get("f")
    listado_cita = Cita.objects.all() 
    if filtro:
            print("Buscado AQUI", filtro)
            listado_cita = Cita.objects.filter(Q(fecha__icontains=filtro))

    elif busqueda:
        listado_cita = Cita.objects.filter(
                Q(nombre_paciente__icontains=busqueda))
  
    cita_reservadas=[]
    
    for listado_cita in listado_cita:
        cita= Cita.objects.get(id_cita=listado_cita.id_cita)
        # paciente = Paciente.objects.get(paciente=listado_cita.paciente) 
        persona = Persona.objects.get(numero_documento=listado_cita.paciente)
      
        cedula = persona.numero_documento
        nombre = persona.nombre + ' ' + persona.apellido
        celular = persona.telefono
        fecha_reservada= cita.fecha
        tratamiento= cita.tratamiento_solicitado
        hora=cita.hora_atencion
        doctor=cita.profesional
        pk_cita = cita.id_cita
        reservacion= cita.estado
        
        cita_reservada= {
                        'nombre_paciente': nombre,
                        'paciente':cedula,
                        'celular':celular,
                        'fecha': fecha_reservada, 
                        'tratamiento_solicitado': tratamiento , 
                        'hora_atencion': hora,  
                        'profesional':doctor , 
                        'id_cita':pk_cita,      
                        'estado':reservacion 
                        
        }
        
        cita_reservadas.append(cita_reservada)
        
    return render(request, "listado_citas.html", {'cita_reservadas': cita_reservadas,})

# "calendario_usuario.html"-->|A NIVEL USUARIO
class CalendarioUsuario(LoginMixin, ListView):
    model = Cita
    template_name = 'calendario_usuario.html'

# def calendario_usuario(request):
#     from datetime import date, timedelta
#     d = date(2022, 1, 1)
#     # d += timedelta(days=6 - d.weekday()) # First Sunday
   
#     listado_cita = Cita.objects.all()
#     cita_reservadas = []
#     while d.year != 2023:
#         for listado_cita in listado_cita:
#             cita= Cita.objects.get(id_cita=listado_cita.id_cita)
#             persona = Persona.objects.get(numero_documento=listado_cita.paciente)
      
#             cedula = persona.numero_documento
#             nombre = persona.nombre + ' ' + persona.apellido
#             celular = persona.telefono
#             fecha_reservada= cita.fecha
#             tratamiento= cita.tratamiento_solicitado
#             hora=cita.hora_atencion
#             doctor=cita.profesional
#             pk_cita = cita.id_cita
#             reservacion= cita.estado
            
#             cita_reservada= {
#                             'nombre_paciente': nombre,
#                             'paciente':cedula,
#                             'celular':celular,
#                             'fecha': fecha_reservada, 
#                             'tratamiento_solicitado': tratamiento , 
#                             'hora_atencion': hora,  
#                             'profesional':doctor , 
#                             'id_cita':pk_cita,      
#                             'estado':reservacion ,
#                             'start':d,
#                             'end':d
                            
#             }
#             cita_reservadas.append(cita_reservada)
        
       
#         return render(request, "calendario_usuario.html", {'cita_reservadas': cita_reservadas, })


    # def get_queryset(self):
    #     queryset = self.model.objects.filter(
    #         estado=True)
    #     return queryset

#<--Vista intermedia usado para restringir accesos-->
def cita_vista(request, id_cita):
   try:
        cita = Cita.objects.get(id_cita=id_cita)
        cedula = cita.paciente
        persona = Persona.objects.get(numero_documento=cedula)
        ci_persona = persona.numero_documento
        ci_user = Usuario.objects.get(numero_documento=ci_persona)
        nro_documento = ci_user.numero_documento
        persona_user = ci_user.usuario
        # user = Usuario.objects.filter(usuario=request.user.usuario)
        # cedula_user=user.usuario

        nombre = persona.nombre + ' ' + persona.apellido

        data = {
            'form': CitaUsuario(instance=cita),
            'persona': persona,
            'id_cita': id_cita,
            'ci_user': ci_user,
            'nro_documento': nro_documento,
            # 'cedula_user':cedula_user

        }
        if persona_user == request.user.usuario:
            print ("es el id_ del usuario", id_cita)
            return redirect("/agendamiento/usuario_changeCita/%s"%(id_cita))
            # 
            # return render(request, "usuario_changeCita.html", data) 
        else:
            return render(request, "cita_vista.html", data)
   except Usuario.DoesNotExist:
       if TypeError:
           return render(request, "cita_sin_usuario.html")
       else:
            return render(request, "cita_sin_usuario.html")
        
        

def calendario_mensaje (request):
    return render (request, "calendario_mensaje.html")

#----------------HORARIO------------------------------
def agregar_hora(request):
    # hora= Horario.objects.filter(hora=hora)
   # horario_form= HoraForm()
    
    data = {
        'form': HoraForm(),
        # 'hora': hora
    }
    
    if request.method == "POST":
        formulario = HoraForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            # if formulario.hora <= 21:
            #     messages.success (request,'Las citas no se reservan después de las 21 p.m. del día')
               
                
                data["mensaje"] = "Registrado correctamente"
                formulario.save()
        # else:
        #     data["form"] = formulario

    return render(request, "agregar_hora.html", data)


#<--listado de hora
def listar_hora(request):
    
    horarios = Horario.objects.all()


    return render(request, "horarios_lista.html", {
        'horarios': horarios})

#<---Eliminar hora


def eliminar_hora(request, id_hora):
    try:
        horarios = Horario.objects.get(id_hora=id_hora)
        horarios.delete()
      
        messages.success(request, "Eliminado")

        return render(request, "horarios_lista.html")

    except Horario.DoesNotExist:
        raise Http404(
            "No se puede eliminar. Dado que ya se Elimino")

#-->REDIRECCIONES
# --> Esta es una template de redirección para el calendario
def calendario_vista(request):
    return render(request, "calendar.html")

# --> Esta es una template de redirección para el horario reservado

def horario_reservado(request):
    return render(request, "horario_reservado.html")

# --> Esta es una template de redirección para el horario duplicado

def horario_duplicado(request):
    return render(request, "horario_duplicado.html")

###############
def agendar_tratamiento_asignado(id_paciente, codigo_tratamiento):
    """
    Procedimiento que registra el tratamiento que el paciente solicito agendar
    (copia el registro de PacienteTratamientoAgendado a TratamientoConfirmado, en esta con estado='Pendiente')
    """
    paciente_obt = Paciente.objects.get(id_paciente=id_paciente)
    tratamiento_obt = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)

    tratamiento_agendado = TratamientoConfirmado.objects.create(
                                                                paciente=paciente_obt,
                                                                tratamiento=tratamiento_obt,
                                                                estado='Pendiente'
    )
    paciente_tratamiento = PacienteTratamientoAsignado.objects.filter(paciente=paciente_obt, tratamiento=tratamiento_obt).delete()

def confirmar_cita_tratamiento(id_paciente, codigo_tratamiento):
    """
    Procedimiento que modifica el estado del registro de TratamientoConfirmado a estado='Agendado'
    una vez que esl paciente confirma la cita, pero aun no paga por ella
    """
    paciente_obt = Paciente.objects.get(id_paciente=id_paciente)
    tratamiento_obt = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)

    tratamiento_agendado = TratamientoConfirmado.objects.filter(
                                                                paciente=paciente_obt,
                                                                tratamiento=tratamiento_obt,
    )
    tratamiento_agendado.update(estado='Agendado')

def eliminar_tratamiento_asignado(id_paciente, codigo_tratamiento):
    """
    Procedimiento que elimina el tratamiento asignado al paciente (de la tabla 
    PacienteTramientoAsignado) una vez que se haya realizado el agendamiento de 
    cita con el tratamiento que fue asignado por el Odontologo
    """
    paciente_obt = Paciente.objects.get(id_paciente=id_paciente)
    tratamiento_obt = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
    paciente_tratamiento = PacienteTratamientoAsignado.objects.get(paciente=paciente_obt, tratamiento=tratamiento_obt)
    id_paciente = paciente_tratamiento.paciente.get_id()
    paciente_tratamiento.delete()
