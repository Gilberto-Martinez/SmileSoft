from http.client import HTTPResponse
import json
from django.shortcuts import render
from django.views.generic import  TemplateView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from gestion_administrativo.models import TratamientoConfirmado
from gestion_agendamiento.models import Cita
from gestion_reporte.form import ReporteTratamientoForm
# Create your views here.


class ListadoTratamientoView(ListView):
    model = TratamientoConfirmado
    # context_object_name = ''
    template_name='tratamiento_cita.html'
    
    def get_queryset(self): 
        return self.model.objects.filter(estado='Agendado')
    
    def get(self, request , *args, **kwargs):
        if request.is_ajax():
            listado_tratamiento_mas_solicitado= []
            for estado in self.queryset():
                diccionario_tratamiento={}
                diccionario_tratamiento['tratamiento']= estado.tratamiento
                listado_tratamiento_mas_solicitado.append(diccionario_tratamiento)
            data=json.dumps(listado_tratamiento_mas_solicitado)
            print(data)
            return HTTPResponse(data, 'application/json')
        else:
            return render(request, self.template_name)
    
    





class ReporteTratamientoView(TemplateView):
    template_name = 'reporte_tratamiento.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # data = {}
        action = request.POST['action']
        if action == 'search_report':
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            search = Cita.objects.all()
            if len(start_date) and len(end_date):
                search = search.filter(fecha__range=[start_date, end_date])
            for s in search:
                
                data.append([
                    s.id_cita,
                    s.tratamiento_solicitado,
                    s.fecha.strftime('%Y-%m-%d'),
                   
                ])
        else:
            data['error'] = 'Ha ocurrido un error'
     
        return render(request, "reporte_tratamiento.html", data, safe=False)
   # <!-->
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte'
        context['entity'] = 'Reportes'
        # context['list_url'] = reverse_lazy('reporte_tratamiento')
        context['form'] = ReporteTratamientoForm()
        return context




def tratamiento_mas_solicitado(request):
    
    # citas_agendadas= TratamientoConfirmado.objects.get(estado="Agendado")
    
    
    
    
    listado_cita = Cita.objects.all() 
    
    cita_reservadas=[]
    
    for lista_cita in  listado_cita:
        
        cita= Cita.objects.get(id_cita=lista_cita.id_cita)
        fecha_reservada= cita.fecha
        tratamiento= cita.tratamiento_solicitado or cita.tratamiento_simple

    cita_reservada= {
                    
                        'fecha': fecha_reservada, 
                        'tratamiento_solicitado': tratamiento , 
                        # 'id_cita':id_cita,
                        
        }
        
    cita_reservadas.append(cita_reservada)
        
    return render(request, "tratamiento_mas_solicitado.html", {'cita_reservadas': cita_reservadas})
    
    
    