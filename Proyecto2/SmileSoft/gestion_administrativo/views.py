from audioop import reverse
from multiprocessing import context
from pyexpat import model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import *
from django.contrib import messages
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

# Permisos
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.core.exceptions import ObjectDoesNotExist


############################ LISTADOS ###############################################


class PersonaList(ListView):
    model = Persona
    template_name = 'listar_persona.html'

    # @method_decorator(permission_required('gestion_administrativo.view_persona', login_url="/panel_control/error/"))
    # def dispatch(self, *args, **kwargs):
    #     return super(PersonaList, self).dispatch(*args, **kwargs)
    
    def get(self, request, **kwargs):
        # verificamos permisos
        if not self.request.user.has_perm('gestion_administrativo.view_persona'):
            return render(request, "panel_control/error.html")
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

class FuncionarioList(ListView):
    model = Funcionario
    template_name = 'listar_funcionario.html'
    
    # @method_decorator(permission_required('gestion_administrativo.view_funcionario', login_url="/panel_control/error/"))
    # def dispatch(self, *args, **kwargs):
    #     return super(FuncionarioList, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        # verificamos permisos
        if not self.request.user.has_perm('gestion_administrativo.view_funcionario'):
            return render(request, "panel_control/error.html")
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


class PacienteList(ListView):
    model = Paciente
    template_name = 'listar_paciente.html'
    
    # @method_decorator(permission_required('gestion_administrativo.view_paciente', login_url="/panel_control/error/"))
    # def dispatch(self, *args, **kwargs):
    #     return super(PacienteList, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        # verificamos permisos
        if not self.request.user.has_perm('gestion_administrativo.view_paciente'):
            return render(request, "panel_control/error.html")
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)
    
  

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

class EspecialistaSaludList(ListView):
    model = EspecialistaSalud
    template_name = 'listar_especialista_salud.html'
    
    # @method_decorator(permission_required('gestion_administrativo.view_especialista_salud', login_url="/panel_control/error/"))
    # def dispatch(self, *args, **kwargs):
    #     return super(EspecialistaSaludList, self).dispatch(*args, **kwargs)

    
    def get(self, request, **kwargs):
        # verificamos permisos
        if not self.request.user.has_perm('gestion_administrativo.view_especialista_salud'):
            return render(request, "panel_control/error.html")
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)



class ProveedorList(ListView):
    model = Proveedor
    template_name = 'listar_proveedor.html'
    
    # @method_decorator(permission_required('gestion_administrativo.view_proveedor', login_url="/panel_control/error/"))
    # def dispatch(self, *args, **kwargs):
    #     return super(ProveedorList, self).dispatch(*args, **kwargs)

    
    def get(self, request, **kwargs):
        # verificamos permisos
        if not self.request.user.has_perm('gestion_administrativo.view_proveedor'):
            return render(request, "panel_control/error.html")
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


class CargoList(ListView):
    model = Cargo
    template_name = 'listar_cargo.html'
    
    # @method_decorator(permission_required('gestion_administrativo.view_cargo', login_url="/panel_control/error/"))
    # def dispatch(self, *args, **kwargs):
    #     return super(CargoList, self).dispatch(*args, **kwargs)

    
    def get(self, request, **kwargs):
        # verificamos permisos
        if not self.request.user.has_perm('gestion_administrativo.view_cargo'):
            return render(request, "panel_control/error.html")
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


########################### INSERCION #################################################


class PersonaCreate(CreateView):
    model = Persona
    template_name = 'agregar_persona.html'
    success_url = reverse_lazy('listar_persona')
    form_class = PersonaForm
    second_form_class = FuncionarioForm
    third_form_class = PacienteForm
    fourth_form_class = EspecialistaSaludForm

    def get_context_data(self, **kwargs):
        context = super(PersonaCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        if 'form3' not in context:
            context['form3'] = self.third_form_class(self.request.GET)
        if 'form4' not in context:
            context['form4'] = self.fourth_form_class(self.request.GET)
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)  # self.form_class(request.POST)
        # self.second_form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        form3 = self.third_form_class(request.POST)
        form4 = self.fourth_form_class(request.POST)
        if form.is_valid():
            if form2.is_valid():
                # persona = form.save(commit=False)
                # persona.es_funcionario = True
                # persona.save()
                persona = form.save()
                funcionario = form2.save(commit=False)
                funcionario.numero_documento = persona
                funcionario.save()
                form2.save_m2m()
            if form3.is_valid():
                # persona = form.save(commit=False)
                # persona.es_paciente = True
                # persona.save()
                persona = form.save()
                paciente = form3.save(commit=False)
                paciente.numero_documento = persona
                paciente.save()
                messages.success(
                    request, " ✅Se ha agregado  correctamente")
            if form4.is_valid():
                # persona = form.save(commit=False)
                # persona.es_especialista_salud = True
                # persona.save()
                persona = form.save()
                especialista_salud = form4.save(commit=False)
                especialista_salud.numero_documento = persona
                especialista_salud.save()
            return HttpResponseRedirect(self.success_url)
        else:
            # messages.error('No ha ingresado los datos correctamente')
            return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3, form4=form4))


class FuncionarioCreate(CreateView):
    model = Funcionario
    template_name = 'agregar_funcionario.html'
    second_form_class = PersonaForm
    # third_form_class = Cargo
    success_url = reverse_lazy('listar_funcionario')
    form_class = FuncionarioForm

    def get_context_data(self, **kwargs):
        context = super(FuncionarioCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        # if 'form3' not in context:
            # context['form3'] = self.third_form_class(self.request.GET)
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        # form3 = self.third_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            funcionario = form.save(commit=False)
            persona = form2.save()
            funcionario.numero_documento = persona
            funcionario.save()
            form.save_m2m()
            messages.success(request, "Funcionario agregado")
            return HttpResponseRedirect(self.success_url)
        else:
            messages.error(request, "No funciona")
            print('NO ENTRAAAAA')
            return self.render_to_response(self.get_context_data(form=form, form2=form2))


# class EspecialistaSaludCreate(CreateView):
#     model = EspecialistaSalud
#     template_name = 'agregar_especialista_salud.html'
#     second_form_class = PersonaForm
#     success_url = reverse_lazy('listar_especialista_salud')
#     form_class = EspecialistaSaludForm

#     def get_context_data(self, **kwargs):
#         context = super(EspecialistaSaludCreate,
#                         self).get_context_data(**kwargs)
#         if 'form' not in context:
#             context['form'] = self.form_class(self.request.GET)
#         if 'form2' not in context:
#             context['form2'] = self.second_form_class(self.request.GET)
#         return context

#     @method_decorator(csrf_protect)
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object
#         # form = EspecialistaSaludForm(request.POST)
#         # form2 = PersonaForm(request.POST)
#         # # data = {
#         # #     'form': EspecialistaSaludForm(),
#         # #     'form2': PersonaForm()
#         # # }
#         form = self.form_class(request.POST)
#         form2 = self.second_form_class(request.POST)
        
#         if form.is_valid() and form2.is_valid():
#             especialista_salud = form.save(commit=False)
#             persona = form2.save()
#             especialista_salud.numero_documento = persona
#             especialista_salud.save()
#             form.save_m2m()
#             messages.success(request, " ✅ Agregado correctamente")
#             print('ENTRAAAAA')
#             return HttpResponseRedirect(self.success_url)
#         else:
#             print('NO ENTRAAAAA')
#             return self.render_to_response(self.get_context_data(form=form, form2=form2))

class EspecialistaSaludCreate(CreateView):
    model = EspecialistaSalud
    template_name = 'agregar_especialista_salud.html'
    second_form_class = PersonaForm
    success_url = reverse_lazy('listar_especialista_salud')
    form_class = EspecialistaSaludForm

    def get_context_data(self, **kwargs):
        context = super(EspecialistaSaludCreate,
                        self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = EspecialistaSaludForm(request.POST)
        form2 = PersonaForm(request.POST)
        data = {
            'form': EspecialistaSaludForm(),
            'form2': PersonaForm()
        }
        if form.is_valid() and form2.is_valid():
            especialista_salud = form.save(commit=False)
            especialista_salud.numero_documento = form2.save()
            especialista_salud.save()
            form.save_m2m()
            messages.success(request, " ✅ Agregado correctamente")
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))


class ProveedorCreate(CreateView):
    model = Proveedor
    template_name = 'agregar_proveedor.html'
    form_class = ProveedorForm
    success_url = reverse_lazy('listar_proveedor')

    def get_context_data(self, **kwargs):
        context = super(ProveedorCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        data = {
            'form': ProveedorForm()
        }
        if form.is_valid():
            form.save()
            messages.success(request, " ✅ Proveedor agregado correctamente")
            # data['mensaje'] = "Agregado correctamente"
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CargoCreate(CreateView):
    model = Cargo
    template_name = 'agregar_cargo.html'
    form_class = CargoForm
    success_url = reverse_lazy('listar_cargo')

    def get_context_data(self, **kwargs):
        context = super(CargoCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        # data = {
        #     'form': ProveedorForm()
        #     }
        if form.is_valid():
            form.save()
            messages.success(request, " ✅ Cargo Agregado correctamente")
            # data['mensaje'] = "Agregado correctamente"
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class SuccessView(TemplateView):
    template_name = 'success.html'


class SuccessError(TemplateView):
    template_name = 'mostrar_mensaje_error.html'


class PacienteCreate(CreateView):
    model = Paciente
    template_name = 'agregar_paciente.html'
    second_form_class = PersonaForm
    success_url = reverse_lazy('listar_paciente')
    form_class = PacienteForm

    def get_context_data(self, **kwargs):
        context = super(PacienteCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)  # self.form_class
        form2 = self.second_form_class(request.POST)  # self.second_form_class
        data = {
            'form': PacienteForm(),
            'form2': PersonaForm()
        }
        if form.is_valid() and form2.is_valid():
            paciente = form.save(commit=False)
            paciente.numero_documento = form2.save()
            paciente.save()
            messages.success(
                request, " ✅Se ha agregado  correctamente")
            # messages.success(request,"Paciente agregado")

            data['mensaje'] = "Agregado correctamente"
            return HttpResponseRedirect(self.success_url)
        else:
            print('NO ENTRA en form')
            messages.error(
                request, "Ha ocurrido un error, vuelva a intentarlo")
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

############################### ACTUALIZACIONES #############################


class PersonaUpdate(UpdateView):

    model = Persona
    second_model = Funcionario
    third_model = Paciente
    fourt_model = EspecialistaSalud
    template_name = 'modificar_persona.html'
    form_class = PersonaUpdateForm
    second_form_class = FuncionarioForm
    third_form_class = PacienteForm
    fourt_form_class = EspecialistaSaludForm
    success_url = reverse_lazy('listar_persona')

    def get_context_data(self, **kwargs):
        context = super(PersonaUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        persona = self.model.objects.get(numero_documento=pk)
        
        if 'form' not in context:
            context['form'] = self.form_class()
        try:
            funcionario = self.second_model.objects.get(numero_documento=persona.numero_documento)
        except ObjectDoesNotExist:# Si funcionario con ese numero de documento no existe cargara un formulario de funcioanrio sin datos
            context['form2'] = self.second_form_class()
        else: # Si funcionario con ese numero de documento existe cargara los datos del funcionario extraidos se la base de datos al contexto
            if 'form2' not in context:
                context['form2'] = self.second_form_class(instance=funcionario)

        try:
            paciente = self.third_model.objects.get(numero_documento=persona.numero_documento)
        except ObjectDoesNotExist:
            context['form3'] = self.third_form_class()
        else:
            if 'form3' not in context:
                context['form3'] = self.third_form_class(instance=paciente)

        try:
            especialista_salud = self.fourt_model.objects.get(numero_documento=persona.numero_documento)
        except ObjectDoesNotExist:
            context['form4'] = self.fourt_form_class()
        else:
            if 'form4' not in context:
                context['form4'] = self.fourt_form_class(instance=especialista_salud)
        context['numero_documento'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_pers = kwargs['pk']
        persona = self.model.objects.get(numero_documento=id_pers)
        form = self.form_class(request.POST, instance=persona)
        try:
            funcionario = self.second_model.objects.get(numero_documento=persona.numero_documento)
        except ObjectDoesNotExist:# Si funcionario no existe mostrara el formulario de Funcionario Vacio
            form2 = self.second_form_class(request.POST)
        else: # Si funcionario existe mostrará los datos del funcionario extraidos de la base de datos en el formulario
            form2 = self.second_form_class(request.POST, instance=funcionario)

        try:
            paciente = self.third_model.objects.get(numero_documento=persona.numero_documento)
        except ObjectDoesNotExist:
            form3 = self.third_form_class(request.POST)
        else:
            form3 = self.third_form_class(request.POST, instance=paciente)

        try:
            especialista_salud = self.fourt_model.objects.get(numero_documento=persona.numero_documento)
        except ObjectDoesNotExist:
            form4 = self.fourt_form_class(request.POST)
        else:
            form4 = self.fourt_form_class(request.POST, instance=especialista_salud)

        if form.is_valid():
            persona = form.save()
            
            if form2.is_valid():
                funcionario = form2.save(commit=False)
                funcionario.numero_documento = persona
                funcionario.save()
                form2.save_m2m()
               
            if form3.is_valid():
                paciente = form3.save(commit=False)
                paciente.numero_documento = persona
                paciente.save()
               
            if form4.is_valid(): # Aun falta implementar
                especialista_salud = form4.save(commit=False)
                especialista_salud.numero_documento = persona
                especialista_salud.save()
            messages.success(request, " ✅ Modificado correctamente")
            return HttpResponseRedirect(self.get_success_url())
        
        else:
            return HttpResponseRedirect(self.get_success_url())


class FuncionarioUpdate(UpdateView):
    model = Funcionario
    second_model = Persona
    template_name = 'modificar_funcionario.html'
    form_class = FuncionarioForm
    second_form_class = PersonaUpdateForm
    success_url = reverse_lazy('listar_funcionario')

    def get_context_data(self, **kwargs):
        context = super(FuncionarioUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        funcionario = self.model.objects.get(id_funcionario=pk)
        persona = self.second_model.objects.get(
            numero_documento=funcionario.numero_documento)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=persona)
        context['id_funcionario'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_func = kwargs['pk']
        funcionario = self.model.objects.get(id_funcionario=id_func)
        persona = self.second_model.objects.get(
            numero_documento=funcionario.numero_documento)
        form = self.form_class(request.POST, instance=funcionario)
        form2 = self.second_form_class(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, " ✅ Modificado correctamente")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return super().get(request, *args, **kwargs)


class EspecialistaSaludUpdate(UpdateView):
    model = EspecialistaSalud
    second_model = Persona
    template_name = 'modificar_especialista_salud.html'
    form_class = EspecialistaSaludForm
    second_form_class = PersonaUpdateForm
    success_url = reverse_lazy('listar_especialista_salud')
    error_url = reverse_lazy('mensaje_error')

    def get_context_data(self, **kwargs):
        context = super(EspecialistaSaludUpdate,
                        self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        especialista_salud = self.model.objects.get(id_especialista_salud=pk)
        persona = self.second_model.objects.get(
            numero_documento=especialista_salud.numero_documento)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=persona)
        context['id_especialista_salud'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_especialista = kwargs['pk']
        especialista_salud = self.model.objects.get(
            id_especialista_salud=id_especialista)
        persona = self.second_model.objects.get(
            numero_documento=especialista_salud.numero_documento)
        form = self.form_class(request.POST, instance=especialista_salud)
        form2 = self.second_form_class(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, " ✅ Modificado correctamente")
            return HttpResponseRedirect(self.get_success_url())
        else:
            if not form.is_valid():
                print('form no es valido')
            if not form2.is_valid():
                print('form2 no es valido')
            print('No entraaaaaaaaaaa')
            return HttpResponseRedirect(self.error_url)


class PacienteUpdate(UpdateView):
    model = Paciente
    second_model = Persona
    template_name = 'modificar_paciente.html'
    form_class = PacienteForm
    second_form_class = PersonaUpdateForm
    success_url = reverse_lazy('listar_paciente')

    def get_context_data(self, **kwargs):
        context = super(PacienteUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        paciente = self.model.objects.get(id_paciente=pk)
        persona = self.second_model.objects.get(
            numero_documento=paciente.numero_documento)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=persona)
        context['id_paciente'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_pac = kwargs['pk']
        paciente = self.model.objects.get(id_paciente=id_pac)
        persona = self.second_model.objects.get(
            numero_documento=paciente.numero_documento)
        form = self.form_class(request.POST, instance=paciente)
        form2 = self.second_form_class(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

#  <----------------Exclusivo de Configuracion/ Paciente-------------------------------->

def editar_persona(request, numero_documento):

    numero_documento = Persona.objects.get(numero_documento=numero_documento)

    data = {
        'form': PersonaUpdateForm(instance=numero_documento)
    }
    if request.method == 'POST':
        formulario = PersonaForm(
            data=request.POST, instance=numero_documento, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["form"] = formulario
            messages.success(request, " ✅Se ha realizado su cambio")
            print("ENTRA AQUI !!!!!!!!!!!!!!!!!!!!!")

        else:
            messages.error(request, "No se ha realizado su cambio")
            print("NOOOOOOOOOOO modifica!!!!!!!!!!!!!!!!!!!!!")

    return render(request, "editar_persona.html", data)

###
# @permission_required('gestion_administrativo.editar_antecedente', login_url="/panel_control/error/",)
def editar_antecedente(request, numero_documento):
    persona = Paciente.objects.get(numero_documento=numero_documento)
    data = {
        'form': PacienteForm(instance=persona)
    }
    if request.method == 'POST':
        formulario = PacienteForm(
            data=request.POST, instance=persona, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            print("ENTRA AQUI !!!!!!!!!!!!!!!!!!!!!", data)
            data["form"] = formulario
            messages.success(request, " ✅Se ha realizado su cambio")
            return render(request, "panel_control/cambio_exitoso.html")
        else:
            messages.error(request, "No se ha realizado su cambio")
            print("NOOOOOOOOOOO modifica!!!!!!!!!!!!!!!!!!!!!")

    return render(request, "editar_antecedente.html", data)
###
#  <--------------------------------------------------------------------->


class ProveedorUpdate(UpdateView):
    model = Proveedor
    template_name = 'modificar_proveedor.html'
    form_class = ProveedorUpdateForm
    success_url = reverse_lazy('listar_proveedor')

    def get_context_data(self, **kwargs):
        context = super(ProveedorUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['ruc'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_prov = kwargs['pk']
        proveedor = self.model.objects.get(ruc=id_prov)
        form = self.form_class(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, " ✅ Modificado correctamente")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class CargoUpdate(UpdateView):
    model = Cargo
    template_name = 'modificar_cargo.html'
    form_class = CargoForm
    success_url = reverse_lazy('listar_cargo')

    def get_context_data(self, **kwargs):
        context = super(CargoUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['nombre'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cargo = kwargs['pk']
        cargo = self.model.objects.get(nombre=id_cargo)
        form = self.form_class(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, " ✅ Modificado correctamente")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


# def modificar_funcionario(request, numero_documento):
#     persona = Persona.objects.get(numero_documento=numero_documento)
#     funcionario = Funcionario.objects.get(numero_documento=persona.numero_documento)
#     success_url = reverse_lazy('correcto')

#     data = {
#         'form': PersonaForm(instance=persona),
#         'form2': FuncionarioForm(instance=funcionario)
#     }
#     if request.method == 'POST':
#         formulario = PersonaForm(
#             data=request.POST, instance=persona, files=request.FILES)
#         formulario2 = FuncionarioForm(
#             data=request.POST, instance=funcionario, files=request.FILES)
#         if formulario.is_valid() and formulario2.is_valid():
#             formulario.save()
#             formulario2.save()
#             print("ENTRA AQUI !!!!!!!!!!!!!!!!!!!!!")
#             data['mensaje'] = "Modificado correctamente"
#         else:
#             messages.error(request, "Contraseñas no coinciden")
#             print("NO modifica")
#     return HttpResponseRedirect(success_url)

############################### ELIMINACION ###################################
class PersonaDelete(DeleteView):
    model = Persona
    template_name = 'eliminar_persona.html'
    success_url = reverse_lazy('listar_persona')


class FuncionarioDelete(DeleteView):
    model = Funcionario
    template_name = 'eliminar_funcionario.html'
    success_url = reverse_lazy('listar_funcionario')


class EspecialistaSaludDelete(DeleteView):
    model = EspecialistaSalud
    template_name = 'eliminar_especialista_salud.html'
    success_url = reverse_lazy('listar_especialista_salud')


class PacienteDelete(DeleteView):
    model = Paciente
    template_name = 'eliminar_paciente.html'
    success_url = reverse_lazy('listar_paciente')


class ProveedorDelete(DeleteView):
    model = Proveedor
    template_name = 'eliminar_proveedor.html'
    success_url = reverse_lazy('listar_proveedor')


class CargoDelete(DeleteView):
    model = Cargo
    template_name = 'eliminar_cargo.html'
    success_url = reverse_lazy('listar_cargo')


################################################################################
################################################################################
@permission_required('gestion_administrativo.add_pacientetratamientoasignado', login_url="/panel_control/error/",)
def asignar_tratamiento (request, numero_documento):
    # success_url ='mensajes/mensaje_exitoso_asignar_tratamiento.html'
    data= {
        'form' : PacienteAsignadoForm(),
        'object' : Persona.objects.get(numero_documento=numero_documento)
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
            # return HttpResponseRedirect(success_url)
        else:
            data["form"]=formulario
            data['object']=persona
            print('NO ENTRAAAAA')
            
    return render(request,"asignar_tratamiento.html",data)

# class TratamientoAsignadoCreate(CreateView):
#     model = PacienteTratamientoAsignado
#     second_model = Persona
#     template_name = 'asignar_tratamiento.html'
#     form_class = PacienteAsignadoForm
#     second_form_class = PersonaTratamientoForm
#     success_url = reverse_lazy('listar_paciente2')

#     def get_context_data(self, **kwargs):
#         context = super(TratamientoAsignadoCreate, self).get_context_data(**kwargs)
#         num = self.kwargs.get('numero_documento', 0)
#         persona = self.second_model.objects.get(numero_documento=num)
#         if 'form' not in context:
#             context['form'] = self.form_class(self.request.GET)
#         if 'object' not in context:
#             context['object'] = self.second_model(self.request.GET, instance=persona)
#         context['numero_documento'] = num
#         return context

#     @method_decorator(csrf_protect)
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object
#         num = kwargs['numero_documento']
#         form = self.form_class(request.POST)
#         persona = self.second_model.objects.get(numero_documento=num)
#         object = self.second_model(request.POST, instance=persona)
#         if form.is_valid():
#             paciente = Paciente.objects.get(numero_documento=num)
#             tratamientos = form.save(commit=False)
#             tratamientos.paciente = paciente
#             tratamientos.save()
#             form.save_m2m()
#             return HttpResponseRedirect(self.success_url)
#         else:
#             return self.render_to_response(self.get_context_data(form=form, object=object))


