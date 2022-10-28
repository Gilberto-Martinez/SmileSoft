from datetime import datetime
from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
from django.shortcuts import render
from gestion_roles.forms import *
from webapp.forms import *
from .forms import *
from django.contrib import messages
from django.http import (
    Http404, HttpResponseRedirect,)
from django.db.models import Q 
from django.views.generic import ListView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView, DetailView
from gestion_administrativo.models import PacienteTratamientoAsignado
from gestion_administrativo.forms import *
from gestion_historial_clinico.views import guardar_historial_clinico
from gestion_agendamiento.models import Cita

# ***Vista de Agregar Rol
# @permission_required('gestion_tratamiento.agregar_tratamiento', login_url="/panel_control/error/",)
def agregar_tratamiento (request):
    data= {
        'form' : TratamientoForm(),
        'form2' : TratamientoCategoriaForm()
    }

    if request.method== "POST":
        form = TratamientoForm(data = request.POST, files= request.FILES)
        form2 = TratamientoCategoriaForm(data = request.POST, files= request.FILES)
        if form.is_valid() and form2.is_valid():
            tratamiento = form.save()
            categoria = form2.save(commit=False)
            categoria.tratamiento = tratamiento
            categoria.save()
            data["mensaje"]="Registrado correctamente"
            messages.success(request,'Agregado correctamente✅')
            print('aquiiiiiiiiiiiiii ENTRAAAAA')
            return redirect('/tratamiento/listar_tratamiento/')
        else:
            data["form"]=form
            data["form2"]=form2
            print('NO ENTRAAAAA')

    return render(request,"tratamiento/agregar_tratamiento.html",data)
#------------------------ Lista de pacientes para asignación de tratamientos -----------------------
class PacienteList2(ListView):
    model = Paciente
    template_name = 'listar_paciente2.html'
    # @method_decorator(permission_required('gestion_administrativo.view_paciente', login_url="/panel_control/error/"))
    # def dispatch(self, *args, **kwargs):
    #     return super(PacienteList2, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        # verificamos permisos
        if not self.request.user.has_perm('gestion_administrativo.view_paciente'):
            return render(request, "panel_control/error.html")
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


# -----------------------------------------------------------------------------------------------
# ***Vista de listar Tratamiento
def listar_tratamiento(request):
    busqueda = request.POST.get("q")
    listado_tratamientos = Tratamiento.objects.all()

    if busqueda:
        listado_tratamientos = Tratamiento.objects.filter(
            Q(nombre_tratamiento__icontains=busqueda))
        print("AQUI ESTA ENTRANDO Y buscando", {
              'listado_tratamientos': listado_tratamientos})
    else:
        print("Buscado AQUI",)
        
    tratamientos=[]
    for listado in listado_tratamientos:
        tratamiento = Tratamiento.objects.get(codigo_tratamiento=listado.codigo_tratamiento)
        codigo_tratamiento = tratamiento.codigo_tratamiento
        nombre=tratamiento.nombre_tratamiento
        # tratamiento_elegido = lista.tratamiento_solicitado or lista.tratamiento_simple
        detalle= tratamiento.descripcion_tratamiento
        monto= '{:,}'.format(tratamiento.precio).replace(',','.')
       
        lista_tratamientos={ 
                            'codigo_tratamiento' : codigo_tratamiento,
                            'nombre_tratamiento': nombre,
                            'descripcion_tratamiento': detalle,
                            'precio':monto,
                           }
        tratamientos.append(lista_tratamientos)
    return render(request, "tratamiento/listar_tratamientos.html", {'tratamientos': tratamientos})


def asignar_tratamientos(request, id_paciente):
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    data= {
        'form' : PacienteAsignadoForm(instance=paciente),
        'paciente': paciente
    }
    # persona = Persona.objects.get(numero_documento=numero_documento)
    if request.method== "POST":
        form= PacienteAsignadoForm(data = request.POST, instance=paciente,files= request.FILES)
        if form.is_valid():
            form.save()
            # form.save_m2m()
            messages.success(request, ('✅'))
            # return render(request, "tratamiento/listar_tratamientos_asignados/%s"%(id_paciente))
            return redirect('/tratamiento/listar_tratamientos_asignados/%s'%(id_paciente))

        else:
            data["form"]=form
            data['paciente']=paciente
    return render(request,"tratamiento/asignar_tratamiento.html",data)


def listar_tratamiento_asignado(request, id_paciente):
    """
    Lista los tratamientos asigandos a un paciente en especifico. Muestra el precio de cada tratamiento.
    Además de eso la template correspondiente a esta función tiene lo siguiente:
        - La opción de Agregar mas tratamientos asigandos o eliminarlos.
        - Permite confirmar los tratamientos a fin de proceder al cobro de las mismas
    """
    listado_tratamientos_asig = PacienteTratamientoAsignado.objects.all()
    paciente = Paciente.objects.get(id_paciente=id_paciente)
  
    tratamientos_asignados = []
    precio_total = 0
    id_paciente_tratamiento = ''

    for tratamiento_asig in listado_tratamientos_asig:
        if str(tratamiento_asig.get_paciente()) == str(id_paciente):
            id_paciente_tratamiento = tratamiento_asig.id_tratamiento_asig
            cod_tratamiento = tratamiento_asig.get_tratamiento()
            nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            precio_total = precio_total + nuevo_tratamieto.precio
            tratamientos_asignados.append(nuevo_tratamieto)
            
         

    precio_total = '{:,}'.format(precio_total).replace(',','.')

    return render (request,"tratamiento/listar_tratamientos_asignados.html",{
                                                                            'tratamientos_asignados':tratamientos_asignados,
                                                                            'paciente':paciente,
                                                                            'precio_total':precio_total,
                                                                            'id_paciente_tratamiento':id_paciente_tratamiento,
                                                                            }
                    )


def listar_tratamientos_pendientes(request):
    tratamientos_conf = TratamientoConfirmado.objects.filter(estado="Pagado")
    tratamientos_pendientes = []

    for tratamiento_conf in tratamientos_conf:
        id_tratamiento_conf = tratamiento_conf.get_id_tratamiento()
        paciente = Paciente.objects.get(id_paciente=tratamiento_conf.paciente.get_id())
        # persona = Persona.objects.get(numero_documento=paciente.numero_documento)
        numero_documento = paciente.numero_documento
        nombre = paciente.numero_documento.nombre
        apellido = paciente.numero_documento.apellido
        tratamiento = Tratamiento.objects.get(codigo_tratamiento=tratamiento_conf.get_tratamiento())
        nombre_tratamiento = tratamiento.nombre_tratamiento
        cita = Cita.objects.get(id_cita=tratamiento_conf.id_cita)
        fecha_atencion = cita.fecha
        hora = cita.hora_atencion.hora
        profesional = cita.profesional.numero_documento.nombre+" "+cita.profesional.numero_documento.apellido
        fecha_pasada = verificar_fecha_hora_agendamiento(cita.id_cita)
        tratamiento_pendiente = {
                                'id_tratamiento_conf':id_tratamiento_conf,
                                'numero_documento':numero_documento,
                                'nombre':nombre,
                                'apellido':apellido,
                                'nombre_tratamiento':nombre_tratamiento,
                                'fecha_atencion':fecha_atencion,
                                'hora':hora,
                                'profesional':profesional,
                                'fecha_pasada':fecha_pasada,
                                'id_cita':cita.id_cita
                                }
        tratamientos_pendientes.append(tratamiento_pendiente)
    return render (request,"tratamiento/listar_tratamientos_pendientes.html",{
                                                                            'tratamientos_pendientes':tratamientos_pendientes,
                                                                            }
                    )

def eliminar_tratamiento_asignado(request, id_pac_tratamiento, cedula):
    paciente_tratamiento = PacienteTratamientoAsignado.objects.get(id_tratamiento_asig=id_pac_tratamiento)
    id_paciente = paciente_tratamiento.paciente.get_id()
    paciente_tratamiento.delete()
    return redirect('/tratamiento/listar_tratamientos_asignados/%s'%(id_paciente))

# def categoria_tratamiento (request):
#     tratamientos= Tratamiento.objects.all()
  
#     tratamientos_por_categoria= []

#     for indice in tratamientos_por_categoria:
#         tratamiento = Tratamiento.objects.get(codigo_tratamiento=indice.get_tratamiento())
#         categoria= TratamientoCategoria.objects.get(categoria_tratamiento=indice.codigo_tratamiento)
        
#         nombre_tratamiento = tratamiento.nombre_tratamiento
#         tratamiento_categorizado= {
                                
#                                 'nombre_tratamiento':nombre_tratamiento
                              
#                                 }
#         tratamientos_pendientes.append(tratamiento_pendiente)
#     return render (request,"tratamiento/listar_tratamientos_pendientes.html",{
#                                                                             'tratamientos_pendientes':tratamientos_pendientes,
#                                                                             }
#                     )
    

class TratamientoCategoriaList (ListView):
    model = TratamientoCategoria
    template_name = 'listar_tratamiento_categoria.html'
# -----------------------------------------------------------------------------------------------

# ***Vista de Modificar Tratamiento


# @permission_required('gestion_tratamiento.modificar_tratamiento', login_url="/panel_control/error/",)
def modificar_tratamiento(request, codigo_tratamiento):
    tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
    tratamiento_categoria = TratamientoCategoria.objects.get(tratamiento=tratamiento)

    data= {
        'form': TratamientoUpdateForm(instance=tratamiento),
        'form2' : TratamientoCategoriaForm(instance=tratamiento_categoria),
        'tratamiento': tratamiento
    }
    if request.method == 'POST':
        form = TratamientoForm(data=request.POST, instance=tratamiento, files=request.FILES)
        form2 = TratamientoCategoriaForm(data=request.POST, instance=tratamiento_categoria, files=request.FILES)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, "Modificado ✅")
            print("ENTRA AQUI !!!!!!!!!!!!!!!!!!!!!")
            data['mensaje'] = "Modificado correctamente"
            return redirect("/tratamiento/listar_tratamiento/")
            
        else:
            messages.error(request, "Algo ha salido Mal, por favor verifique nuevamente")
            print("NOOOOOOOOOOO modifica!!!!!!!!!!!!!!!!!!!!!")

    return render(request, "tratamiento/modificar_tratamiento.html", data)


# -----------------------------------------------------------------------------------------------
# ***Vista de Eliminar Tratamiento
# @permission_required('gestion_tratamiento.eliminar_tratamiento', login_url="/panel_control/error/",)
def eliminar_tratamiento(request, codigo_tratamiento):
    try:
        tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
        tratamiento.delete()
        # listado_tratamientos = Tratamiento.objects.all()
        messages.success(request, "Tratamiento eliminado con exito")
        return redirect("/tratamiento/listar_tratamiento/")
    except Tratamiento.DoesNotExist:
        raise Http404("No se puede eliminar el Tratamiento indicado. Dado que ya se Elimino")



# class TratamientoDelete(DeleteView):
#     model = Tratamiento
#     template_name = 'eliminar_tratamiento.html'
#     success_url = reverse_lazy('listar_tratamientos')

class DetalleTratamientosAsignados(DetailView):
    model = PacienteTratamientoAsignado
    template_name= 'mostrar_tratamientos_asignados.html'

    # def get_object(self):
    #     try:
    #         paciente = Paciente.objects.get(numero_documento= )
    #         instance = self.model.objects.get(paciente = )
    #     return super().get_object(queryset)

def mostrar_tratamiento_asignado (request, numero_documento):
    success_url ='mensajes/mensaje_exitoso_asignar_tratamiento.html'
    paciente_asig=Paciente.objects.get(numero_documento=numero_documento)
    persona_asig = Persona.objects.get(numero_documento=numero_documento)
    data= {
        'object' : Persona.objects.get(numero_documento=numero_documento),
        'object' : Paciente.objects.get(numero_documento=numero_documento),
        'object2' : PacienteTratamientoAsignado.objects.get_queryset()
    }
    persona = Persona.objects.get(numero_documento=numero_documento)
    if request.method== "POST":
        formulario= PacienteAsignadoForm(data = request.POST, files= request.FILES)
        if formulario.is_valid():
            paciente = Paciente.objects.get(numero_documento=numero_documento)
            tratamientos = formulario.save(commit=False)
            tratamientos.paciente = paciente
            tratamientos.save()
            formulario.save_m2m()
            data["mensaje"]="Tratamiento asignado correctamente"
            messages.success(request, (
                'Agregado correctamente!'))
            return HttpResponseRedirect(success_url)
        else:
            data["form"]=formulario
            data['object']=persona
            print('NO ENTRAAAAA')
    data["object"]=persona_asig
    data["object2"]=paciente_asig
            
    return render(request,"tratamiento/mostrar_tratamientos_asignados.html",data)

def mostrar_tratamiento_asignado (request, numero_documento):
    paciente = Paciente.objects.get(numero_documento=numero_documento)
    paciente_asignado = PacienteTratamientoAsignado.objects.get(paciente=paciente.numero_documento)

    data= {
        'form': PacienteAsignadoForm(instance=paciente_asignado)
    }
    if request.method == 'POST':
        form = PacienteAsignadoForm(
            data=request.POST, instance=paciente_asignado, files=request.FILES)
        if form.is_valid():
            
            #formulario.save()
            
            messages.success(request, "Modificado")       
            print("ENTRA AQUI !!!!!!!!!!!!!!!!!!!!!")
                  
            data['mensaje'] = "Modificado correctamente"
            
        else:
            messages.error(request, "Algo ha salido Mal, por favor verifique nuevamente")
            print("NOOOOOOOOOOO modifica!!!!!!!!!!!!!!!!!!!!!")

    return render("tratamiento/mostrar_tratamientos_asignados.html", data)


def ver_mis_tratamientos_pendientes(request, numero_documento):
    tratamientos_conf = TratamientoConfirmado.objects.filter(estado="Pagado")
    tratamientos_pendientes = []
    odontologo = EspecialistaSalud.objects.get(numero_documento=numero_documento)
    profesional = odontologo.numero_documento.nombre+" "+odontologo.numero_documento.apellido

    for tratamiento_conf in tratamientos_conf:
        id_cita = tratamiento_conf.id_cita
        cita = Cita.objects.get(id_cita= id_cita)
        
        if str(cita.profesional.numero_documento) == str(numero_documento):
            id_tratamiento_conf = tratamiento_conf.get_id_tratamiento()
            paciente = Paciente.objects.get(id_paciente=tratamiento_conf.paciente.get_id())
            cedula = paciente.numero_documento
            nombre = paciente.numero_documento.nombre
            apellido = paciente.numero_documento.apellido
            tratamiento = Tratamiento.objects.get(codigo_tratamiento=tratamiento_conf.get_tratamiento())
            nombre_tratamiento = tratamiento.nombre_tratamiento
            # cita = Cita.objects.get(id_cita=tratamiento_conf.id_cita)
            fecha_atencion = cita.fecha
            hora = cita.hora_atencion.hora
            fecha_pasada = verificar_fecha_hora_agendamiento(cita.id_cita)
            tratamiento_pendiente = {
                                    'id_tratamiento_conf':id_tratamiento_conf,
                                    'numero_documento':cedula,
                                    'nombre':nombre,
                                    'apellido':apellido,
                                    'nombre_tratamiento':nombre_tratamiento,
                                    'fecha_atencion':fecha_atencion,
                                    'hora':hora,
                                    'fecha_pasada':fecha_pasada,
                                    'id_cita':id_cita,
                                    }
            tratamientos_pendientes.append(tratamiento_pendiente)
    return render (request,"tratamiento/listar_mis_tratamientos_pendientes.html",{
                                                                            'tratamientos_pendientes':tratamientos_pendientes,
                                                                            'profesional':profesional,
                                                                            }
                    )

def verificar_fecha_hora_agendamiento(id_cita):
    cita = Cita.objects.get(id_cita=id_cita)
    now = datetime.now()
    fecha_actual = now.date()
    hora_actual = now.time()

    fecha_cita = str(cita.fecha)
    fecha_cita = datetime.strptime(fecha_cita, "%Y-%m-%d")
    resultado = relativedelta( fecha_actual, fecha_cita)
    horas = resultado.hours

    respuesta = False

    # print('Diferencia entre horas: ', horas)

    if cita.fecha < fecha_actual:
        respuesta = True
    else:
        if cita.fecha == fecha_actual:
            # if cita.hora_atencion.hora 
            pass

    return respuesta

# """ #BORRADOR
# class InsumoAsignado(UpdateView):
#     model = Tratamiento
#     # second_model = Persona
#     template_name = 'modificar_tratamiento_asignado.html'
#     form_class = TratamientoForm
#     # second_form_class = PersonaUpdateForm
#     # success_url = reverse_lazy('listar_paciente')
#     def get_context_data(self, **kwargs):
#         context = super(InsumoAsignado, self).get_context_data(**kwargs)
#         pk = self.kwargs.get('pk', 0)
#         tratamiento = self.model.objects.get(codigo_tratamiento=pk)
#         # persona = self.second_model.objects.get(numero_documento=paciente.numero_documento)

#         if 'form' not in context:
#             context['form'] = self.form_class(instance=tratamiento)
#         # if 'form2' not in context:
#             # context['form2'] = self.second_form_class(instance=persona)
#         context['codigo_tratamiento'] = pk
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object
#         id_trat = kwargs['pk']
#         tratamiento = self.model.objects.get(codigo_tratamiento=id_trat)
#         cod_tratamiento = tratamiento.codigo_tratamiento
#         # persona = self.second_model.objects.get(numero_documento=paciente.numero_documento)
#         # cedula = paciente.numero_documento
#         form = self.form_class(request.POST, instance=tratamiento)
#         # form2 = self.second_form_class(request.POST, instance=persona)
#         if form.is_valid():
#             form.save()
#             #form2.save()
#             return redirect("/tratamiento/listar_insumos_asignados/%s"%(cod_tratamiento))
#         else:
#             return self.render_to_response(self.get_context_data(form=form)) """


# def listar_insumos_asignado(request, cod_tratamiento):
#     listado_insumos = TratamientoInsumo.objects.all()
#     persona = Persona.objects.get(numero_documento=cedula)
#     paciente = Paciente.objects.get(numero_documento=cedula)
#     id_paciente = paciente.id_paciente

#     tratamientos_asignados = []
#     precio_total = 0
#     id_paciente_tratamiento = ''
#     for insumo in listado_insumos:
#         if str(insumo.get_paciente()) == str(cedula):
#             id_paciente_tratamiento = tratamiento.id
#             cod_tratamiento = tratamiento.get_tratamiento()
#             nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
#             precio_total = precio_total + nuevo_tratamieto.precio
#             tratamientos_asignados.append(nuevo_tratamieto)

#     precio_total = '{:,}'.format(precio_total).replace(',','.')

#     return render (request,"tratamiento/listar_tratamientos_asignados.html",{
#                                                                             'tratamientos_asignados':tratamientos_asignados,
#                                                                             'persona':persona,
#                                                                             'precio_total':precio_total,
#                                                                             'id_paciente_tratamiento':id_paciente_tratamiento,
#                                                                             'id_paciente':id_paciente
#                                                                             }
#                     )


def confirmar_tratamiento(request, id_tratamiento_conf):
    resultado = TratamientoConfirmado.objects.filter(id_tratamiento_conf=id_tratamiento_conf).update(estado='Realizado')
    guardar_historial_clinico(id_tratamiento_conf)
    return redirect('/tratamiento/listar_tratamientos_pendientes/')

# ------------- Pantallas de mensajes ------------------------------- #
def preguntar_confirmacion(request,id_tratamiento_conf):
    tratamiento_conf = TratamientoConfirmado.objects.get(id_tratamiento_conf=id_tratamiento_conf)
    cita = Cita.objects.get(id_cita=tratamiento_conf.id_cita)

    now = datetime.now()
    fecha_actual = now.date()
    hora_actual = now.time()

    fecha_cita = str(cita.fecha)
    fecha_cita = datetime.strptime(fecha_cita, "%Y-%m-%d")
    resultado = relativedelta( fecha_actual, fecha_cita)
    horas = resultado.hours

    print('Diferencia entre horas: ', horas)

    if cita.fecha < fecha_actual:
        return render(request, 'mensajes/fecha_cita_pasada.html',{'id_cita':tratamiento_conf.id_cita})
    else:
        if cita.fecha == fecha_actual:
            # if cita.hora_atencion.hora 
            pass
        
    return redirect( '/tratamiento/mostrar_mensaje_confirmacion/%s' %(id_tratamiento_conf))

def mostrar_mensaje_confirmacion(request,id_tratamiento_conf):
    return render(request,'mensajes/mostrar_mensaje_confirmacion.html',{'id_tratamiento_conf':id_tratamiento_conf}) 


# #############################################
# #asignar insumo esto está en gestión_inventario_insumo


# def asignar_insumos(request, codigo_tratamiento):
#     tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
#     data= {
#         'form' : TratamientoInsAsignadoForm(instance=tratamiento),
#         'tratamiento': tratamiento
#     }
#     # persona = Persona.objects.get(numero_documento=numero_documento)
#     if request.method== "POST":
#         form= TratamientoInsAsignadoForm(data = request.POST, instance=tratamiento,files= request.FILES)
#         if form.is_valid():
#             form.save()
#             # form.save_m2m()
#             # messages.success(request, (
#             #     'Agregado correctamente!'))
#             return redirect("/insumo/listar_insumos_asignados/%s"%(codigo_tratamiento))
#         else:
#             data["form"]=form
#             data['tratamiento']=tratamiento
#     return render(request,"tratamiento/asignar_insumo.html",data)