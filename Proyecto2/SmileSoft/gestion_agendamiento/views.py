from asyncio.windows_events import NULL
from django.utils.html import conditional_escape as esc
from datetime import date, timedelta
from calendar import HTMLCalendar, day_name
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from webapp.mixins import LoginMixin
from django.db.models import Q
from .forms import *
# Create your views here.
from django.contrib import messages
from django.http import Http404
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


# <--Agregar cita-->|A nivel SISTEMA (Verificado)
def agregar_cita(request, id_paciente):
    """Esta función permite al Asistente agendarle una cita con un TRATAMIENTO SIMPLE """
    try:
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
        print("----------------------Agendamiendo del lado del ASISTENTE-----------------------------")
        print("-------------------------------------", nombre, "este es el año------------------",edad)
        data = {
            'form': CitaUsuario(),
            'persona': persona,
        }

        if request.method == "POST":
            formulario = CitaUsuario(data=request.POST, files=request.FILES)
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
                                if cita.hora_atencion == c.hora_atencion and cita.fecha==c.fecha and cita.profesional==c.profesional and paciente != c.paciente:
                                        #print("el numero de la semana  es", nro_semana)
                                        respuesta = "YA EXISTE"
                                        return render(request, 'horario_reservado.html')
                                else: 
                                    # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos
                                    if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional :
                                            respuesta = "Reservado"
                                            # mensaje = "DUPLICADO"
                                            messages.success(request, ('Cita no registrada'))
                                            return render(request, 'cita_duplicada.html')
                                    else:
                                           # Cuando se realiza MAS DE 1 CITA, la misma cita con hora y fecha igual
                                        if paciente== c.paciente and cita.fecha==c.fecha:
                                            respuesta = "Duplicado"
                                            messages.success(request, ('Ya se ha reservado con anterioridad en la misma fecha, pero con un odontólogo distinto'))
                                            return render(request, 'cita_noAutoagendada.html') 
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
                    codigo_tratamiento = cita.tratamiento_simple.tratamiento.codigo_tratamiento
                    tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
                    cita.tratamiento_solicitado = tratamiento
                    
                    print("|||||||||||||CITA GUARDADA DEL PACIENTE QUE TIENE USUARIO||||||||||------------------")
                    # cita.celular = nro_telefonico
                    
                    cita.save()
                    agendar_tratamiento_asignado(id_paciente, codigo_tratamiento, cita.id_cita)
                    if cita.estado == True:
                        confirmar_cita_tratamiento(cita.id_cita)
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


#<--Agendar-->|A nivel SISTEMA, del Lado del Odontólogo (Verificado)
def agendar_cita(request, id_paciente, codigo_tratamiento):
    """
    Esta función permite al Asistente agendarle una cita a un paciente sobre 
    un tratamiento que el Odontologo le haya asignado
    """
    tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
    tratamiento_cat = TratamientoCategoria.objects.get(tratamiento=tratamiento)
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    nombre = persona.nombre + ' ' + persona.apellido
    # ci_persona= persona.numero_documento
    # usuario=Usuario.objects.get(numero_documento=ci_persona)
    # nro_telefonico = persona.telefono
    edad = persona.obtener_edad()
    cita = Cita.objects.all()

    print("----------------------Agendamiendo del lado del ODONTÓLOGO-----------------------------")
    print(nombre, "este es el año------------------",edad)
    print("---------------------------------------------------------------------------------------")


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
            cita.tratamiento_simple = tratamiento_cat
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
                            if cita.hora_atencion == c.hora_atencion and cita.fecha==c.fecha and cita.profesional==c.profesional and paciente != c.paciente:
                                    #print("el numero de la semana  es", nro_semana)
                                respuesta = "YA EXISTE"
                                return render(request, 'horario_reservado.html')
                            else: 
                                # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales iguales 
                                if paciente== c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha==c.fecha and cita.profesional == c.profesional :
                                    respuesta = "Duplicado"
                                    messages.success(request, ('Cita Duplicada'))
                                    return render(request, 'cita_duplicada.html')
                                else:
                                           # Cuando se realiza MAS DE 1 CITA, la misma cita con hora y fecha igual, y con Odontologos Diferentes, QUIERE DECIR QUE NO SE AUTOAGENDO EL PACIENTE SINO QUE CEDIO A OTRO, Y COMO ES LA MISMA HORA ES UN CASO IMPOSIBLE
                                        if paciente== c.paciente and cita.fecha==c.fecha and cita.profesional != c.profesional :
                                            respuesta = "Reservado"
                                            messages.success(request, ('La cita NO fue registrada'))
                                            return render(request, 'cita_noAutoagendada.html')               
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
                agendar_tratamiento_asignado(id_paciente, codigo_tratamiento, cita.id_cita)
                if cita.estado == True:
                    confirmar_cita_tratamiento(cita.id_cita)
                messages.success(request, ('✅Agregado correctamente!'))
                print('aquiiiiiiiiiiiiii ENTRAAAAA',)
                return redirect("/agendamiento/listado_citas/")
        else:
            messages.error(request, ('La cita no ha sido registrada'))
            data["form"] = formulario
            print('NO ENTRAAAAA')
    return render(request, "agendar_cita.html", data)


# <--Agregar cita de un MENOR DE EDAD- o {Paciente SIN USUARIO}->|A nivel SISTEMA (Verificado)
# @permission_required('gestion_agendamiento.addcita_cita_usuario', login_url="/panel_control/error/",)
def addcita_cita_usuario(request, id_paciente):
    """ Esta función permite al Asistente 
    agendarle un Paciente Menor de Edad o Sin Usuario """
     
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    nombre = persona.nombre + ' ' + persona.apellido
    nro_telefonico = persona.telefono
    edad = persona.obtener_edad()
    fecha = Cita.objects.all()
    hora_atencion = Horario.objects.all()
    data = {
        'form': CitaUsuario(),
        'persona': persona,
        'id_paciente': id_paciente,
        'hora_atencion': hora_atencion,
    }

    if request.method == "POST":
        formulario = CitaUsuario(data=request.POST, files=request.FILES)
        respuesta = "NO EXISTE"
        print("------------||||PACIENTE SIN USUARIO||||||------------------")
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
                            if cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional and paciente != c.paciente:
                                #print("el numero de la semana  es", nro_semana)
                                respuesta = "YA EXISTE"
                                return render(request, 'horario_reservado.html')
                            else:
                                # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos
                                if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional:
                                    respuesta = "Reservado"
                                    messages.success(request, ('Cita Duplicada'))
                                    return render(request, 'horario_duplicado.html')
                                else:
                                        # Cuando se realiza MAS DE 1 CITA, la misma cita con hora y fecha igual
                                    if paciente== c.paciente and cita.fecha==c.fecha:
                                        respuesta = "Duplicado"
                                        messages.success(request, ('La Cita NO Fue Registrada'))
                                        return render(request, 'cita_noReservada.html') 
                        else:
                            if nro_semana >= 5:
                                #"Si es fin de semana emite el msj"
                                messages.success(
                                    request, "Por favor, elija dias entre Lunes a Viernes")
                                return render(request, 'cerrado.html')
                    else:
                        if dia_recibido < actual or hora_recibida < hora_actual:
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
                messages.success(request, ('✅ Cita registrada'))
                return render(request, "aprobado.html")
        else:
            messages.error(request, ('No ha guardado'))
            data["form"] = formulario
            print('NO ENTRAAAAA')

    return render(request, "agregar_cita_usuario.html", data)

# <--***Agregar cita a un {PACIENTE CON USUARIO}***-->|A nivel USUARIO (Verificado)
# @permission_required('gestion_agendamiento.addcita_usuario', login_url="/panel_control/error/",)
def addcita_usuario(request, numero_documento):

    """ Esta función permite agregar una cita para todo aquel que cuente con un USUARIO"""
    try:
        persona = Persona.objects.get(numero_documento=numero_documento)
        # cedula = persona.numero_documento
        paciente = Paciente.objects.get(numero_documento=numero_documento)
        id_paciente = paciente.id_paciente
        nombre = persona.nombre + ' ' + persona.apellido
        print(' A nivel USUARIO/CLIENTE --- > Esta es la cedula: ', numero_documento, 'Este es el id del paciente: ', id_paciente) 
    
        hora_atencion= Horario.objects.all()
        # hora= HoraForm(request.POST)
        
        data = {
            'form': CitaUsuario(),
            'persona': persona,
            'id_paciente': id_paciente,
            'hora_atencion': hora_atencion,
        
        }

        if request.method == "POST":
            formulario = CitaUsuario(data=request.POST, files=request.FILES)
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
                                print("-----------------------------Nivel USUARIO----------------------")                 
                                if cita.hora_atencion == c.hora_atencion and cita.fecha==c.fecha and cita.profesional==c.profesional and paciente != c.paciente:
                                        #print("el numero de la semana  es", nro_semana)
                                        respuesta = "Reservado"
                                        return render(request, 'horario_reservado.html')
                                else: 
                                    # Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos
                                    if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional :
                                            respuesta = "Reservado"
                                            # mensaje = "DUPLICADO"
                                            messages.success(request, ('Cita Duplicada'))
                                            return render(request, 'horario_duplicado.html')
                                    else:
                                            # Cuando se realiza MAS DE 1 CITA, la misma cita con hora y fecha igual
                                        if paciente== c.paciente and cita.fecha==c.fecha:
                                            respuesta = "Duplicado"
                                            messages.success(request, ('Cita No Registrada'))
                                            return render(request, 'cita_noReservada.html') 
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
                    codigo_tratamiento = cita.tratamiento_simple.tratamiento.codigo_tratamiento
                    tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
                    cita.tratamiento_solicitado = tratamiento
                    # cita.estado= reservado
                    cita.save()
                    agendar_tratamiento_asignado(id_paciente, codigo_tratamiento, cita.id_cita)
                    print("###Guarda la CITA  DEL USUARIO REGISTRADO-----------------",cita.estado,"dentro de 6meses" ,fecha_meses, "fecha de CITA", cita.fecha,)
                    messages.success(request, ('✅ Su cita ha sido registrada'))
                    return render(request, "calendario.html")
            else:
                messages.error(request, ('No ha guardado'))
                data["form"] = formulario
                print('NO ENTRAAAAA')
            messages.error(request, ('No ha guardado la cita...........¡Ocurrió un error!'))
        return render(request, "usuario_addCita.html", data)
    except Paciente.DoesNotExist:
        if TypeError:
           return redirect("/agendamiento/roles_multiples/")
       # return render(request, "usuario_paciente.html", data)
        
 # @permission_required('gestion_agendamiento.cambiarCita_usuario', login_url="/panel_control/error/",)
#<--Modificar (Verificado) -> |A NIVEL USUARIO (No se puede BORRAR porque usa el Calendario al EDITAR de lado CLiente)
def cambiarCita_usuario(request, id_cita):
     
    """ Esta función permite Modificar del lado Cliente/Usuario Paciente"""
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
        tratamiento_solicitado= cita.tratamiento_solicitado or cita.tratamiento_simple
        especialista=cita.profesional

        data = {
            'form': CitaUpdateForm(instance=cita),
            'persona': persona,
            'id_cita': id_cita,
            'ci_user':ci_user,
            'nro_documento': nro_documento,
            'id_paciente': id_paciente,
            'estado': reservado,
            'tratamiento_solicitado': tratamiento_solicitado,
            'profesional': especialista
        # 'cedula_user':cedula_user
            
        }
        if request.method == "POST":
            formulario = CitaModificarForm(data=request.POST, instance=cita, files=request.FILES)
            respuesta= "NO EXISTE"
            reservado = cita.estado
            tratamiento_tipo = cita.tratamiento_solicitado
          
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
                    #"""Seis meses despues de la fecha actual"
                    fecha_meses = (datetime.date.today() )+ timedelta(365/2)
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
                            #Obs: El estado no debe influir dado que ya sea True o False si YA ESTA RESERVADO EN LA FECHA Y EL PROFESIONAL , no debe permitir Reservar el mismo dia sin importar que los pacientes sean distintos
                            if cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional and paciente.numero_documento != c.paciente.numero_documento:
                                respuesta = "YA EXISTE"
                                return render(request, 'horario_reservado.html')
                            else:                
                                if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional and (cita.tratamiento_solicitado== c.tratamiento_solicitado or cita.tratamiento_simple== c.tratamiento_simple  ):
                                    respuesta = "NO EXISTE"
                                    print("PASA AQUI---------PERO SALTA")
                                    # messages.success(request, ('No hubo cambios recientes registrados en la cita'))            
                                    # return redirect("/agendamiento/calendario_mensaje/")
                                else:
                                      # SE DA CUANDO YA EXISTE ANTERIORMENTE REGISTRADO Y se quiere volver a elegir la misma fecha, la misma hora y el mismo odontólogo
                                    if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and reservado== False and cita.profesional == c.profesional and (cita.tratamiento_solicitado!= c.tratamiento_solicitado or cita.tratamiento_simple!= c.tratamiento_simple  ):
                                        respuesta = "Duplicado"
                                        print ("Llega a tener diferentes odontologos con diferentes tratamientos con hora diferente")
                                        messages.success(request, ('Cita Duplicada'))
                                        return render(request, 'horario_duplicado.html')
                                    else:
                                        # Cuando se realiza MAS DE 1 CITA, la misma cita con hora y fecha igual
                                        if paciente== c.paciente and cita.fecha==c.fecha and cita.hora_atencion == c.hora_atencion:
                                            respuesta = "Excedido"
                                            print ("Llega a tener diferentes odontologos,sin importar si son tratamientos iguales o distintos")
                                            messages.success(request, ('Ya se ha reservado con anterioridad en la misma fecha, pero con un odontólogo distinto'))
                                            return render(request, 'cita_noReservada.html') 
                                
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
                else:
                    if str(fecha_meses) < dia_recibido:
                        #     # dia_recibido se toma la fecha que ingresa por lo tanto, aca el dia que recibe sera mayor que dentro de 6meses, y fecha_meses sera
                        #     #menor a lo que recibe porque se cuenta desde la fecha actual y no desde la fecha que se ingresa
                        #     # print("---imprime feha en seis meses", anhio)
                        return render(request, 'atencion_fecha.html')
                
                        
                if respuesta== "NO EXISTE":
                    print("Si ya existe salta y guarda")
                    cita.paciente = paciente
                    cita.nombre_paciente = nombre
                    cita.estado=reservado
                    cita.tratamiento_tipo = cita.tratamiento_solicitado
                    cita.profesional:especialista
                    # cita.estado= cambio_estado
                    cita.save()
                    
                    messages.success(request, ('✅ Guardado Correctamente'))            
                    return redirect("/agendamiento/calendario_mensaje/")
               
            else:
                messages.error(request, (' ⚠ No ha guardado'))    
        return render(request, "usuario_changeCita.html", data) 
    except Usuario.DoesNotExist:
       if TypeError:
           return redirect("/agendamiento/modificar_cita_usuario/%s" % (id_cita))
       else:
            return render(request, "cita_sin_usuario.html")


# <--****!!!!Modificar Principal!!!!-->|Cuando Tiene Usuario y no tiene Usuario --> A nivel SISTEMA|  USA EL ODONTOLOGO/ASISTENTE
def modificar_cita(request, id_cita):
      
    """ Esta función permite Modificar del lado Sistema, es la modificación principal"""
    try:
        cita_actual = Cita.objects.get(id_cita=id_cita)
        cedula = cita_actual.paciente.numero_documento
        persona = Persona.objects.get(numero_documento=cedula)
        paciente = Paciente.objects.get(numero_documento=cedula)
        nombre = persona.nombre + ' ' + persona.apellido
        reservado=cita_actual.estado
        tratamiento_solicitado= cita_actual.tratamiento_solicitado or cita_actual.tratamiento_simple
       
        data = {
            'form': CitaUpdateForm(instance=cita_actual),
            'persona': persona,
            'estado':reservado,
            'tratamiento_solicitado': tratamiento_solicitado,
        }

        if request.method == "POST":
            formulario = CitaUpdateForm(data=request.POST, instance=cita_actual, files=request.FILES)
            respuesta= "NO EXISTE"

            if formulario.is_valid():
                cita = formulario.save(commit=False)
                citas= Cita.objects.all()
                reservado=cita.estado
                tratamiento_tipo= cita.tratamiento_solicitado 
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
                                "-----------------------------Modificacion a Nivel Sistema---------------------")
                            print("el estado que entra es", reservado)
                            if cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional and reservado==False and paciente.numero_documento != c.paciente.numero_documento:
                                #print("el numero de la semana  es", nro_semana)
                                respuesta = "YA EXISTE"
                                return render(request, 'horario_reservado.html')
                            else:
                                #Caso especial
                                if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional and (cita.tratamiento_solicitado== c.tratamiento_solicitado or cita.tratamiento_simple== c.tratamiento_simple  ):
                                    respuesta = "NO EXISTE"
                                     #ACA SI ODONTOLOGOS SON IGUALES,con los criterios anteriores, osea
                                    # MISMA FECHA HORA Y TRATAMIENTO , quiere decir que solo se registro DOBLE entonces es el  mismo que ya esta registrado
                                    print("PASA AQUI---------PERO SALTA")
                                    # messages.success(
                                    #     request, ('No hubo cambios recientes registrados en la cita'))
                                else:
                                     # SE DA CUANDO YA EXISTE ANTERIORMENTE REGISTRADO Y se quiere volver a elegir la misma fecha, la misma hora y el mismo odontólogo
                                    if paciente == c.paciente and cita.hora_atencion == c.hora_atencion and cita.fecha == c.fecha and cita.profesional == c.profesional and (cita.tratamiento_solicitado!= c.tratamiento_solicitado or cita.tratamiento_simple!= c.tratamiento_simple  ):
                                        respuesta = "Duplicado"
                                        print ("Llega a tener diferentes odontologos con diferentes tratamientos con hora diferente")
                                        messages.success(request, ('Cita no registrada'))
                                        return render(request, 'cita_duplicada.html')
                                    else:
                                    # Se da Cuando se realiza la misma cita con hora y fecha igual pero con Profesionales distintos EN OTRA CITA YA REGISTRADA
                                        # Cuando se realiza MAS DE 1 CITA, la misma cita con hora y fecha igual

                                        if paciente == c.paciente and cita.fecha == c.fecha and cita.hora_atencion == c.hora_atencion and cita.profesional != c.profesional :
                                            respuesta = "NO EXISTE"
                                            print("ESTA CAMBIANDO DE PROFESIONAL")
                                            # print(
                                            #     "Llega a tener diferentes odontologos,sin importar si son tratamientos iguales o distintos")
                                            messages.success(request, ('El odontólogo ha sido cambiado'))
                                            # return render(request, 'cita_noAutoagendada.html')

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
                    cita.tratamiento_solicitado= tratamiento_tipo
                    cita.save()
                    codigo_tratamiento = cita_actual.tratamiento_simple.tratamiento.codigo_tratamiento
                   # print("el estado que GUARDA ES", cita.estado)
                    if cita.estado == True:
                        print("ENTRA POR AQUI")
                        confirmar_cita_tratamiento(cita.id_cita)
                    if formulario.has_changed() and cita.estado == False: # Si se realizó algun cambio en el formulario y el estado se cambió a false
                        desconfirmar_cita_tratamiento(cita.id_cita)
                    messages.success(request, ('✅ ¡Guardado correctamente!'))            
                    return redirect("/agendamiento/listado_citas/", respuesta)                
            else:
                messages.error(request, "Algo ha salido Mal, por favor verifique nuevamente")
        return render(request, "modificar_cita.html", data)
    except Usuario.DoesNotExist:
            # messages.error(request, " ⚠ Esta persona no cuenta con un usuario propio")
    # return render(request, "autorizar_modificacion.html")
     return redirect("/agendamiento/modificar_cita_usuario/%s" %(id_cita))


# VER EN SOLO LECTURA
def visualizar_cita(request, id_cita):
    """
    Permite visualizar los datos de la cita cuyo tratatmiento ya haya sido realizado
    (TratamientoConfirmado con estado='Realizado') pero en solo lectura, es decir, sin poder modificarlos
    """
    cita = Cita.objects.get(id_cita=id_cita)
    profesional = cita.profesional.numero_documento.nombre +" "+ cita.profesional.numero_documento.apellido
    hora = cita.hora_atencion.hora
    cedula = cita.paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    reservado=cita.estado
    tratamiento_solicitado= cita.tratamiento_solicitado or cita.tratamiento_simple
    
    data = {
        'form': CitaRealizadoForm(instance=cita),
        'persona': persona,
        'estado':reservado,
        'tratamiento_solicitado': tratamiento_solicitado,
        'profesional':profesional,
        'hora':hora,
    }

    if request.method == "POST":
            formulario = CitaRealizadoForm(data=request.POST, instance=cita, files=request.FILES)

    return render(request, "visualizar_cita.html", data)


# VER EN SOLO LECTURA
def visualizar_datos_cita(request, id_cita):
    """
    Permite visualizar los datos de la cita cuyo tratatmiento ya haya sido pagado
    (TratamientoConfirmado con estado='Pagado')y se encuentra a la espera de ser realizada 
    (TratamientoConfirmado con estado='Realizado') pero en solo lectura, es decir, sin poder modificarlos
    """
    cita = Cita.objects.get(id_cita=id_cita)
    profesional = cita.profesional.numero_documento.nombre +" "+ cita.profesional.numero_documento.apellido
    hora = cita.hora_atencion.hora
    cedula = cita.paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    reservado=cita.estado
    tratamiento_solicitado= cita.tratamiento_solicitado or cita.tratamiento_simple
    
    data = {
        'form': CitaPagadaForm(instance=cita),
        'persona': persona,
        'estado':reservado,
        'tratamiento_solicitado': tratamiento_solicitado,
        'profesional':profesional,
        'hora':hora,
    }

    if request.method == "POST":
            formulario = CitaPagadaForm(data=request.POST, instance=cita, files=request.FILES)

    return render(request, "visualizar_datos_cita.html", data)

# <--(NO BORRAR, no se usa pero no Borren) ->Modificar cita DE UNA PERSONA SIN USUARIO o MENOR DE EDAD-->|A nivel SISTEMA 
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
            'form': CitaSistemaForm(instance=cita),
            'persona': persona,
            'estado': reservado,
        }

        if request.method == "POST":
            formulario = CitaSistemaForm(
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
        tratamiento= cita.tratamiento_solicitado or cita.tratamiento_simple
        # tratamiento= cita.tratamiento_simple
        hora=cita.hora_atencion
        doctor=cita.profesional
        pk_cita = cita.id_cita
        reservacion= cita.estado
        tratamiento_paciente = TratamientoConfirmado.objects.get(id_cita=pk_cita)
        estado_tratamiento = False
        if tratamiento_paciente.estado == 'Realizado':
            estado_tratamiento = True
        
        cita_reservada= {
                        'nombre_paciente': nombre,
                        'paciente':cedula,
                        'celular':celular,
                        'fecha': fecha_reservada, 
                        'tratamiento_solicitado': tratamiento , 
                        # 'tratamiento_simple': tratamiento,
                        'hora_atencion': hora,  
                        'profesional':doctor , 
                        'id_cita':pk_cita,      
                        'estado':reservacion,
                        'estado_tratamiento':estado_tratamiento
        }
        
        cita_reservadas.append(cita_reservada)
        
    return render(request, "listado_citas.html", {'cita_reservadas': cita_reservadas})

# "calendario_usuario.html"-->|A NIVEL USUARIO
class CalendarioUsuario(LoginMixin, ListView):
    model = Cita
    template_name = 'calendario_usuario.html'



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

# --> Esta es una template de redirección para cuando el rol es Asistente y Paciente

def roles_multiples(request):
    return render(request, "roles_multiples.html")

############### A NIVEL SISTEMA ####################################
def agendar_tratamiento_asignado(id_paciente, codigo_tratamiento, id_cita):
    """
    Procedimiento que registra el tratamiento que el paciente solicito agendar:
    se crea un registro en TratamientoConfirmado con estado='Agendado'.
    Si existe registro de tratamiento asignado por el odontologo (en PacienteTratmientoAsignado)
    entonces lo elimina
    """
    paciente_obt = Paciente.objects.get(id_paciente=id_paciente)
    tratamiento_obt = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)

    tratamiento_agendado = TratamientoConfirmado.objects.update_or_create(
                                                                paciente=paciente_obt,
                                                                tratamiento=tratamiento_obt,
                                                                estado='Agendado',
                                                                id_cita=id_cita
    )


    try:
        paciente_tratamiento = PacienteTratamientoAsignado.objects.filter(paciente=paciente_obt, tratamiento=tratamiento_obt)
    except paciente_tratamiento.DoesNotExist: # En caso que el paciente se haya autoagendado o lo haya agendado el Asistente y no el Odontologo
        pass
    else: # En caso de que el agendamiento se haya dado con un tratamiento que haya sido asignado por el odontologo
        paciente_tratamiento.delete()

def confirmar_cita_tratamiento(id_cita):
    """
    Procedimiento que modifica el estado del registro de TratamientoConfirmado a estado='Confirmado'
    una vez que esl paciente confirma la cita, pero aun no paga por ella
    """
    tratamiento_agendado = TratamientoConfirmado.objects.get(id_cita=id_cita)
    if tratamiento_agendado.estado == 'Agendado':
        tratamiento_act = TratamientoConfirmado.objects.filter(id_cita=id_cita)
        tratamiento_act.update(estado='Confirmado')


def desconfirmar_cita_tratamiento(id_cita):
    """
    Procedimiento que modifica el estado del registro de TratamientoConfirmado a estado='Agendado'
    si el estado de la Cita cambia a False
    """

    tratamiento_paciente = TratamientoConfirmado.objects.get(id_cita=id_cita)
    if tratamiento_paciente.estado == 'Confirmado':
        tratamiento_act = TratamientoConfirmado.objects.filter(id_cita=id_cita)
        tratamiento_act.update(estado='Agendado')
        cita = Cita.objects.filter(id_cita=id_cita).update(estado= False)


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
