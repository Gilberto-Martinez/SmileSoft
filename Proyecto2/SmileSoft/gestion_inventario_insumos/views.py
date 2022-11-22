import imp
from django.shortcuts import render

# Create your views here.
from email import quoprimime
from email.charset import QP
from tokenize import Name
from unicodedata import name
from django.shortcuts import render
from httplib2 import RETRIES
from urllib3 import encode_multipart_formdata
from gestion_inventario_insumos.utils import render_to_pdf
#from Proyecto2.SmileSoft.gestion_inventario_insumos.models import Insumo
# from gestion_roles.models import Rol
from gestion_roles.forms import *
from webapp.forms import *
#from .forms import *
from django.contrib import messages
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,)
from django.views.generic.list import ListView, View
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q 
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView, DetailView
from gestion_administrativo.forms import *
from gestion_inventario_insumos.forms import *
from gestion_tratamiento.models import TratamientoInsumoAsignado
from gestion_tratamiento.forms import TratamientoInsAsignadoForm
from gestion_tratamiento.models import *
from django.shortcuts import redirect
# ***Vista de Agregar Rol
# @permission_required('gestion_inventario_insumos.agregar_insumo', login_url="/panel_control/error/",)
def agregar_insumo (request):
    
    data= {
        'form' : InsumoForm()
    }
    
    if request.method== "POST":
        formulario= InsumoForm(data = request.POST, files= request.FILES)
        if formulario.is_valid():
            insumo = formulario.save(commit=False)
            #calculo_unitario = insumo.cantidad_insumo * insumo.unidad_x_paquete
            calculo_unitario = insumo.cantidad_insumo * insumo.unidad_x_paquete
            insumo.cantidad_unitaria = calculo_unitario
            insumo.save()
            data["mensaje"]="Registrado correctamente"
            messages.success(request, (' ✅ Insumo Agregado Correctamente!'))
            return redirect("/insumo/listar_insumos/")  
            
            print('aquiiiiiiiiiiiiii ENTRAAAAA')
        else:
            data["form"]=formulario
            print('NO ENTRAAAAA')
            
    return render(request,"insumo/agregar_insumo.html",data)

# -----------------------------------------------------------------------------------------------
#***Vista de listar Insumo


@permission_required('gestion_inventario_insumos.listar_insumo', login_url="/panel_control/error/",)
#funciona pero no es lista
# def listar_insumo(request):
    
#     busqueda=request.POST.get("q")
#     listado_insumos = Insumo.objects.all()
    
#     if busqueda:  
#         listado_insumos =Insumo.objects.filter(Q(nombre_insumo__icontains= busqueda))
#         print("AQUI ESTA ENTRANDO Y buscando", {'listado_insumos':listado_insumos})
#     else:                                                              
#         print("Buscado AQUI",)
        
#     return render (request,"insumo/listar_insumos.html",{'listado_insumos':listado_insumos})
########################################################################################################3
# -----------------------------------------------------------------------------------------------
#listar tratamientos en formato lista[]
def listar_insumo(request):
    busqueda = request.POST.get("q")
    listado_insumos = Insumo.objects.all()

    if busqueda:
        listado_insumos = Insumo.objects.filter(
            Q(nombre_insumo__icontains=busqueda))
        print("AQUI ESTA ENTRANDO Y buscando", {
              'listado_insumos': listado_insumos})
    else:
        print("Buscado AQUI",)
        
    insumos=[]
    for listado in listado_insumos:
        insumo = Insumo.objects.get(codigo_insumo=listado.codigo_insumo)
        codigo_insumo = insumo.codigo_insumo
        nombre=insumo.nombre_insumo
        cantidad_insumo= insumo.cantidad_insumo
        unidad=insumo.unidad
        upcl=insumo.unidad_x_paquete
        ud_unitaria=insumo.ud_unitaria
        stock_minimo= insumo.stock_minimo
        #existencia = si cantidad_unitaria < stock_minimo entoces "en falta" sino "disponible"
        existencia = "Disponible"
        disponible = True
        if insumo.cantidad_unitaria >= insumo.stock_minimo:
            existencia = "Disponible"
            disponible = True
        else:
            existencia = "En Falta"
            disponible = False
        detalle= insumo.descripcion_insumo
        cantidad_unitaria = insumo.cantidad_insumo
        
        monto= '{:,}'.format(insumo.precio).replace(',','.')
       
        lista_insumos={ 
                            'codigo_insumo' : codigo_insumo,
                            'nombre_insumo': nombre,
                            'descripcion_insumo': detalle,
                            'precio':monto,
                            'cantidad_insumo':cantidad_insumo,
                            'unidad':unidad,
                            'unidad_x_paquete':upcl,
                            'cantidad_unitaria':cantidad_unitaria,
                            'ud_unitaria':ud_unitaria,
                            'stock_minimo': stock_minimo,
                            'existencia': existencia, 
                            'disponible': disponible
                            
                           }
        
        insumos.append(lista_insumos)

    return render(request, "insumo/listar_insumos.html", {'insumos': insumos})
  
#----inicio-------------------------------------------------------------#
#                     VISTA DE LISTA CLONADA (No hagan caso. Es una prueba) (lista simple para generar pdf)
#-----------------------------------------------------------------------#
# def listar_insumo_simple(request):
#     busqueda = request.POST.get("q")
#     listado_insumos = Insumo.objects.all()

#     if busqueda:
#         listado_insumos = Insumo.objects.filter(
#             Q(nombre_insumo__icontains=busqueda))
#         print("AQUI ESTA ENTRANDO Y buscando", {
#               'listado_insumos': listado_insumos})
#     else:
#         print("Buscado AQUI",)

#     insumos = []
#     for listado in listado_insumos:
#         insumo = Insumo.objects.get(codigo_insumo=listado.codigo_insumo)
#         codigo_insumo = insumo.codigo_insumo
#         nombre = insumo.nombre_insumo
#         # tratamiento_elegido = lista.tratamiento_solicitado or lista.tratamiento_simple
#         detalle = insumo.descripcion_insumo
#         monto = '{:,}'.format(insumo.precio).replace(',', '.')

#         lista_insumos = {
#             'codigo_insumo': codigo_insumo,
#             'nombre_insumo': nombre,
#             'descripcion_insumo': detalle,
#             'precio': monto,
#         }

#         insumos.append(lista_insumos)

#     # return render(request, "insumo/listar_insumos.html", {'insumos': insumos})
#     return render(request, "insumo/insumo_lista.html", {'insumos': insumos})


  
#-----Es la vista que LLAMA A LA FUNCION PARA GENERAR PDF
class ListaInsumoPDF(View):
    def get(self, request, *args, **kwargs):
        insumos = Insumo.objects.all()
        data={

           'insumos':insumos
        }
        pdf=render_to_pdf('insumo/insumo_lista.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

#----fin-------------------------------------------------------------#
#     
#-----------------------------------------------------------------------#
   
# ***Vista de Modificar Insumos


# @permission_required('gestion_tratamiento.modificar_tratamiento', login_url="/panel_control/error/",)
def modificar_insumo(request, codigo_insumo):
    codigo_insumo = Insumo.objects.get(codigo_insumo=codigo_insumo)

    data= {
        'form': InsumoUpdateForm(instance=codigo_insumo)
    }
    if request.method == 'POST':
        formulario = InsumoForm(
            data=request.POST, instance=codigo_insumo, files=request.FILES)
        if formulario.is_valid():
            
            insumo = formulario.save(commit=False)
            #calculo_unitario = insumo.cantidad_insumo * insumo.unidad_x_paquete
            calculo_unitario = insumo.cantidad_insumo * insumo.unidad_x_paquete
            insumo.cantidad_unitaria = calculo_unitario
            insumo.save()
            
            messages.success(request, " Insumo Modificado Correctamente ✅")
            return redirect("/insumo/listar_insumos/")     
                
        else:
            messages.error(request, "Algo ha salido Mal, por favor verifique nuevamente")
            print("NOOOOOOOOOOO modifica!!!!!!!!!!!!!!!!!!!!!")

    return render(request, "insumo/modificar_insumos.html", data)


# -----------------------------------------------------------------------------------------------
# ***Vista de Eliminar Insumo
# @permission_required('gestion_inventario_insumo.eliminar_insumo', login_url="/panel_control/error/",)
def eliminar_insumo(request, codigo_insumo):
    try:
        insumo = Insumo.objects.get(codigo_insumo=codigo_insumo)
        insumo.delete()
        messages.success(request, " Insumo Eliminado ❌")
        return redirect("/insumo/listar_insumos/")
    except Insumo.DoesNotExist:
        raise Http404("No se puede eliminar el Insumo indicado. Dado que ya se Elimino")

#####################################################################################################

##INSUMOS ASIGNADOS 

def asignar_insumos(request, codigo_tratamiento):
    tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
    nombre= tratamiento.nombre_tratamiento
    data= {
        'form' : TratamientoInsAsignadoForm(instance=tratamiento),
        'tratamiento': tratamiento,
        'nombre':nombre
    }
    # persona = Persona.objects.get(numero_documento=numero_documento)
    if request.method== "POST":
        form= TratamientoInsAsignadoForm(data = request.POST, instance=tratamiento,files= request.FILES)
        if form.is_valid():
            form.save()
            # form.save_m2m()
            messages.success(request, ('✅ Insumo asignado '))
            return redirect("/insumo/listar_insumos_asignados/%s"%(codigo_tratamiento))
            # return redirect("/mensajes/insumo_asignado_exitoso/%s"%(tratamiento.codigo_tratamiento))
        else:
            data["form"]=form
            data['tratamiento']=tratamiento
    return render(request,"insumo/asignar_insumo.html",data)


def listar_insumo_asignado(request, codigo_tratamiento):
    """
    Lista los insumos asignados a un tratamiento en especifico. 
    """
    listado_insumos_asig = TratamientoInsumoAsignado.objects.all()
    tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
    tratamientos_insumos_asignados = []
    # id_tratamiento_insumo = ''
   
    for insumo_asig in listado_insumos_asig:
        if str(insumo_asig.get_tratamiento()) == str(codigo_tratamiento):
            # id_tratamiento_insumo = insumo_asig.id_insumo_asig
            cod_insumo = insumo_asig.get_insumo()
            nuevo_insumo = Insumo.objects.get(codigo_insumo=cod_insumo)
            tratamiento_insumo_asig = {
                                        "insumo":nuevo_insumo,
                                        "tratamiento_insumo_asignado":insumo_asig
            }
            tratamientos_insumos_asignados.append(tratamiento_insumo_asig)


    return render (request,"insumo/listar_insumos_asignados.html",{
                                                                    'tratamientos_insumos_asignados':tratamientos_insumos_asignados,
                                                                    'tratamiento':tratamiento,
                                                                            }
                    )

def editar_cantidad_insumos_asig(request, id_tratamiento_insumo):
    """
    Permite modificar la cantidad de insumos a ser utilizado para un tratamiento en especifico 
    """
    tratamiento_insumo_asignado = TratamientoInsumoAsignado.objects.get(id_insumo_asig=id_tratamiento_insumo)
    codigo_insumo = tratamiento_insumo_asignado.get_insumo()
    insumo = Insumo.objects.get(codigo_insumo=codigo_insumo)
    codigo_tratamiento = int(tratamiento_insumo_asignado.get_tratamiento())
    data= {
        'form' : InsumoAsignadoForm(instance=tratamiento_insumo_asignado),
        'tratamiento_insumo_asignado':tratamiento_insumo_asignado,
        'insumo':insumo,
        'codigo_tratamiento':codigo_tratamiento
    }
    if request.method == "POST":
        form= InsumoAsignadoForm(data = request.POST, instance=tratamiento_insumo_asignado,files= request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, ('✅ Proceso exitoso '))
            return redirect('/insumo/listar_insumos_asignados/%s'%(codigo_tratamiento))
        else:
            data["form"]=form
            data['tratamiento_insumo_asignado']=tratamiento_insumo_asignado
            data["insumo"]=insumo
            data["codigo_tratamiento"]=codigo_tratamiento
            messages.success(request, (' No Guardado '))

    return render (request,"insumo/agregar_cantidad_insumos.html",data
                    )

##########################################################################################################################
######RESTAMOS LA CANTIDAD DEL INSUMO En Contrucción

# def update_cantidad_u(request, Insumo.codigo_insumo, TratamientoInsumoAsignado.cantidad, TratamientoConfirmado.estado):
#         pedido = Pedido.objects.get(id=id_pedido, id_articulo)
#         stock    = Articulo.objects.get(id=id_articulo)
#         cant -= stock
#         stock.save()
#         # articulo.stock = cant
#         return HttpResponseRedirect("/solicitar/lista/")



# def mostrar_insumo_asignado_exitoso(request,codigo_tratamiento):
#     return render(request,"insumo_asignado_exitoso.html",{"codigo_tratamiento":codigo_tratamiento})

# def listar_tratamientos_pendientes(request):
#     tratamientos_conf = TratamientoConfirmado.objects.filter(estado="Confirmado")
#     tratamientos_pendientes = []

#     for tratamiento_conf in tratamientos_conf:
#         id_tratamiento_conf = tratamiento_conf.get_id_tratamiento()
#         paciente = Paciente.objects.get(id_paciente=tratamiento_conf.paciente.get_id())
#         # persona = Persona.objects.get(numero_documento=paciente.numero_documento)
#         numero_documento = paciente.numero_documento
#         nombre = paciente.numero_documento.nombre
#         apellido = paciente.numero_documento.apellido
#         tratamiento = Tratamiento.objects.get(codigo_tratamiento=tratamiento_conf.get_tratamiento())
#         nombre_tratamiento = tratamiento.nombre_tratamiento
#         tratamiento_pendiente = {
#                                 'id_tratamiento_conf':id_tratamiento_conf,
#                                 'numero_documento':numero_documento,
#                                 'nombre':nombre,
#                                 'apellido':apellido,
#                                 'nombre_tratamiento':nombre_tratamiento
#                                 }
#         tratamientos_pendientes.append(tratamiento_pendiente)
#     return render (request,"tratamiento/listar_tratamientos_pendientes.html",{
#                                                                             'tratamientos_pendientes':tratamientos_pendientes,
#                                                                             }
#                     )

# def eliminar_tratamiento_asignado(request, id_pac_tratamiento, cedula):
#     paciente_tratamiento = PacienteTratamientoAsignado.objects.get(id=id_pac_tratamiento)
#     paciente_tratamiento.delete()
#     return redirect('/tratamiento/listar_tratamientos_asignados/%s'%(cedula))


# -----------------------------------------------------------------------------------------------

# ***Vista de Modificar Tratamiento


# @permission_required('gestion_tratamiento.modificar_tratamiento', login_url="/panel_control/error/",)
# def modificar_tratamiento(request, nombre_tratamiento):
#     nombre_tratamiento = Tratamiento.objects.get(nombre_tratamiento=nombre_tratamiento)

#     data= {
#         'form': TratamientoUpdateForm(instance=nombre_tratamiento)
#     }
#     if request.method == 'POST':
#         formulario = TratamientoForm(
#             data=request.POST, instance=nombre_tratamiento, files=request.FILES)
#         if formulario.is_valid():
            
#             formulario.save()
            
#             messages.success(request, "Modificado")       
#             print("ENTRA AQUI !!!!!!!!!!!!!!!!!!!!!")
                  
#             data['mensaje'] = "Modificado correctamente"
            
#         else:
#             messages.error(request, "Algo ha salido Mal, por favor verifique nuevamente")
#             print("NOOOOOOOOOOO modifica!!!!!!!!!!!!!!!!!!!!!")

#     return render(request, "tratamiento/modificar_tratamiento.html", data)


# # -----------------------------------------------------------------------------------------------
# # ***Vista de Eliminar Tratamiento
# # @permission_required('gestion_tratamiento.eliminar_tratamiento', login_url="/panel_control/error/",)
# def eliminar_tratamiento(request, nombre_tratamiento):
#     try:
#         tratamiento = Tratamiento.objects.get(nombre_tratamiento=nombre_tratamiento)
#         tratamiento.delete()
#         listado_tratamientos = Tratamiento.objects.all()
#         messages.success(request, "Eliminado")
#         return render(request, "tratamiento/listar_tratamientos.html", {'listado_tratamientos': listado_tratamientos})
#     except Tratamiento.DoesNotExist:
#         raise Http404("No se puede eliminar el Tratamiento indicado. Dado que ya se Elimino")



# class TratamientoDelete(DeleteView):
#     model = Tratamiento
#     template_name = 'eliminar_tratamiento.html'
#     success_url = reverse_lazy('listar_tratamientos')

# class DetalleInsumosAsignados(DetailView):
#     model = TratamientoInsumoAsignado
#     template_name= 'mostrar_insumos_asignados.html'

    # def get_object(self):
    #     try:
    #         paciente = Paciente.objects.get(numero_documento= )
    #         instance = self.model.objects.get(paciente = )
    #     return super().get_object(queryset)

# def mostrar_insumo_asignado (request, codigo_tratamiento):
#     success_url ='mensajes/mensaje_exitoso_asignar_insumo.html'
#     tratamiento_asig=Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
#     tratamiento_asig = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
#     data= {
#         'object' : Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento),
#         'object' : Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento),
#         'object2' : TratamientoInsumoAsignado.objects.get_queryset()
#     }
#     tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
#     if request.method== "POST":
#         formulario= TratamientoInsAsignadoForm(data = request.POST, files= request.FILES)
#         if formulario.is_valid():
#             tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
#             insumos = formulario.save(commit=False)
#             insumos.tratamiento = tratamiento
#             insumos.save()
#             formulario.save_m2m()
#             data["mensaje"]="Insumo asignado correctamente"
#             messages.success(request, (
#                 'Agregado correctamente!'))
#             return HttpResponseRedirect(success_url)
#         else:
#             data["form"]=formulario
#             data['object']=tratamiento
#             print('NO ENTRAAAAA')
#     data["object"]=tratamiento_asig
#     data["object2"]=tratamiento_asig
            
#     return render(request,"insumo/mostrar_insumos_asignados.html",data)

# def mostrar_insumo_asignado (request, codigo_tratamiento):
#     tratamiento = Tratamiento.objects.get(codigo_tratamiento=codigo_tratamiento)
#     tratamiento_asignado = TratamientoInsumoAsignado.objects.get(tratamiento=tratamiento.codigo_tratamiento)

#     data= {
#         'form': TratamientoInsAsignadoForm(instance=tratamiento_asignado)
#     }
#     if request.method == 'POST':
#         form = TratamientoInsAsignadoForm(
#             data=request.POST, instance=tratamiento_asignado, files=request.FILES)
#         if form.is_valid():
            
#             #formulario.save()
            
#             messages.success(request, "Modificado")       
#             print("ENTRA AQUI !!!!!!!!!!!!!!!!!!!!!")
                  
#             data['mensaje'] = "Modificado correctamente"
            
#         else:
#             messages.error(request, "Algo ha salido Mal, por favor verifique nuevamente")
#             print("NOOOOOOOOOOO modifica!!!!!!!!!!!!!!!!!!!!!")

#     return render("insumo/mostrar_insumos_asignados.html", data)


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
#             return self.render_to_response(self.get_context_data(form=form))


# # def listar_insumos_asignado(request, cod_tratamiento):
# #     listado_insumos = TratamientoInsumo.objects.all()
# #     persona = Persona.objects.get(numero_documento=cedula)
# #     paciente = Paciente.objects.get(numero_documento=cedula)
# #     id_paciente = paciente.id_paciente

# #     tratamientos_asignados = []
# #     precio_total = 0
# #     id_paciente_tratamiento = ''
# #     for insumo in listado_insumos:
# #         if str(insumo.get_paciente()) == str(cedula):
# #             id_paciente_tratamiento = tratamiento.id
# #             cod_tratamiento = tratamiento.get_tratamiento()
# #             nuevo_tratamieto = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
# #             precio_total = precio_total + nuevo_tratamieto.precio
# #             tratamientos_asignados.append(nuevo_tratamieto)

# #     precio_total = '{:,}'.format(precio_total).replace(',','.')

# #     return render (request,"tratamiento/listar_tratamientos_asignados.html",{
# #                                                                             'tratamientos_asignados':tratamientos_asignados,
# #                                                                             'persona':persona,
# #                                                                             'precio_total':precio_total,
# #                                                                             'id_paciente_tratamiento':id_paciente_tratamiento,
# #                                                                             'id_paciente':id_paciente
# #                                                                             }
# #                     )


# def confirmar_tratamiento(request, id_tratamiento_conf):
#     resultado = TratamientoConfirmado.objects.filter(id_tratamiento_conf=id_tratamiento_conf).update(estado='Realizado')
#     guardar_historial_clinico(id_tratamiento_conf)
#     return redirect('/tratamiento/listar_tratamientos_pendientes/')

# # ------------- Pantallas de mensajes ------------------------------- #
# def preguntar_confirmacion(request,id_tratamiento_conf):
#     return redirect( '/tratamiento/mostrar_mensaje_confirmacion/%s' %(id_tratamiento_conf))

# def mostrar_mensaje_confirmacion(request,id_tratamiento_conf):
#     return render(request,'mensajes/mostrar_mensaje_confirmacion.html',{'id_tratamiento_conf':id_tratamiento_conf})
 