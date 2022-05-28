from audioop import reverse
from multiprocessing import context
from pyexpat import model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import *
from django.contrib import messages
from django.views.generic import ListView,CreateView, TemplateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

############################ LISTADOS ###############################################
class PersonaList(ListView):
    model = Persona
    template_name = 'listar_persona.html'


class FuncionarioList(ListView):
    model = Funcionario
    template_name = 'listar_funcionario.html'


class PacienteList(ListView):
    model = Paciente
    template_name = 'listar_paciente.html'


class EspecialistaSaludList(ListView):
    model = EspecialistaSalud
    template_name = 'listar_especialista_salud.html'


class ProveedorList(ListView):
    model = Proveedor
    template_name = 'listar_proveedor.html'


class CargoList(ListView):
    model = Cargo
    template_name = 'listar_cargo.html'

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
        form = self.form_class(request.POST) # self.form_class(request.POST)
        form2 = self.second_form_class(request.POST) # self.second_form_class(request.POST)
        form3 = self.third_form_class(request.POST)
        form4 = self.fourth_form_class(request.POST)
        if form.is_valid():
            print('Validoooooooooooooooooooo el primero')
            if form2.is_valid():
                print('Validoooooooooooooooooooo')
                funcionario = form2.save(commit=False)
                funcionario.numero_documento = form.save()
                funcionario.save()
            if form3.is_valid():
                print('Validoooooooooooooooooooo')
                paciente = form3.save(commit=False)
                paciente.numero_documento = form.save()
                paciente.save()
                messages.success(
                request, " ✅Se ha agregado  correctamente")
            if form4.is_valid():
                print('Validoooooooooooooooooooo')
                especialista_salud = form4.save(commit=False)
                especialista_salud.numero_documento = form.save()
                especialista_salud.save()
            else:
                form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            print('NO ENTRAAAAA')
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
            messages.success(request,"Funcionario agregado")
            return HttpResponseRedirect(self.success_url)
        else:
            messages.error(request,"No funciona")
            print('NO ENTRAAAAA')
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

class EspecialistaSaludCreate(CreateView):
    model = EspecialistaSalud
    template_name = 'agregar_especialista_salud.html'
    second_form_class = PersonaForm
    success_url = reverse_lazy('listar_especialista_salud')
    form_class = EspecialistaSaludForm

    def get_context_data(self, **kwargs):
        context = super(EspecialistaSaludCreate, self).get_context_data(**kwargs)
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
            data['mensaje'] = "Agregado correctamente"
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
            # data['mensaje'] = "Agregado correctamente"
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))



class  CargoCreate(CreateView):
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
        form = PacienteForm(request.POST) #self.form_class
        form2 = PersonaForm(request.POST)#self.second_form_class
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
            messages.error(request,"Ha ocurrido un error, vuelva a intentarlo")
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

############################### ACTUALIZACIONES #############################
class PersonaUpdate(UpdateView):
    model = Persona
    second_model = Funcionario
    template_name = 'modificar_persona.html'
    form_class = PersonaUpdateForm
    second_form_class = FuncionarioForm
    success_url = reverse_lazy('listar_persona')

    def get_context_data(self, **kwargs):
        context = super(PersonaUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        persona = self.model.objects.get(numero_documento=pk)
        funcionario = self.second_model.objects.get(numero_documento=persona.numero_documento)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=funcionario)
        context['numero_documento'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_pers = kwargs['pk']
        persona = self.model.objects.get(numero_documento=id_pers)
        funcionario = self.second_model.objects.get(numero_documento=persona.numero_documento)
        form = self.form_class(request.POST, instance=persona)
        form2 = self.second_form_class(request.POST, instance=funcionario)
        if form.is_valid():
            print('Validoooooooooooooooooooo el primero')
            if form2.is_valid():
                print('Validoooooooooooooooooooo')
                form.save()
                form2.save()
            else:
                form.save()
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
        pk = self.kwargs.get('pk',0)
        funcionario = self.model.objects.get(id_funcionario=pk)
        persona = self.second_model.objects.get(numero_documento=funcionario.numero_documento)
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
        persona = self.second_model.objects.get(numero_documento=funcionario.numero_documento)
        form = self.form_class(request.POST, instance=funcionario)
        form2 = self.second_form_class(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
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
        context = super(EspecialistaSaludUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        especialista_salud = self.model.objects.get(id_especialista_salud=pk)
        persona = self.second_model.objects.get(numero_documento=especialista_salud.numero_documento)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=persona)
        context['id_especialista_salud'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_especialista = kwargs['pk']
        especialista_salud = self.model.objects.get(id_especialista_salud=id_especialista)
        persona = self.second_model.objects.get(numero_documento=especialista_salud.numero_documento)
        form = self.form_class(request.POST, instance=especialista_salud)
        form2 = self.second_form_class(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
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
        pk = self.kwargs.get('pk',0)
        paciente = self.model.objects.get(id_paciente=pk)
        persona = self.second_model.objects.get(numero_documento=paciente.numero_documento)
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
        persona = self.second_model.objects.get(numero_documento=paciente.numero_documento)
        form = self.form_class(request.POST, instance=paciente)
        form2 = self.second_form_class(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

class ProveedorUpdate(UpdateView):
    model = Proveedor
    template_name = 'modificar_proveedor.html'
    form_class = ProveedorUpdateForm
    success_url = reverse_lazy('listar_proveedor')

    def get_context_data(self, **kwargs):
        context = super(ProveedorUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
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
        pk = self.kwargs.get('pk',0)
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