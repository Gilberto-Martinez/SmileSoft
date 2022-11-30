from http.client import HTTPResponse
from django.http import ( HttpResponse,)
from ipaddress import summarize_address_range
import json
import random
import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.views.generic import  TemplateView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from gestion_inventario_insumos.models import Insumo
from gestion_administrativo.models import TratamientoConfirmado
from gestion_agendamiento.models import Cita
from gestion_reporte.form import ReporteTratamientoForm
    
from django.db.models import Count    

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
            return HttpResponse(data, 'application/json')
        else:
            return render(request, self.template_name)
    
    

# def tratamiento_reporte (request):
#     tratamiento_reporte= TratamientoConfirmado.objects.filter(estado='Agendado')
  
    # print (tratamiento_reporte,' es AGENDADO......', conteo)
    
    # return render('reporte_tratamiento.html',conteo)




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


def insumos_reporte(request):
    qs= Insumo.objects.all().values()
    
    data= pd.DataFrame(qs)
    
    # data_insumos = pd.read_csv("insumos_listado.csv", sep=",")
    # data_insumos.head()
    # DF_Nombre = qs['nombre_insumo']
    # print(data)
    
    context={
        'df': data.to_html,
        
        'describe':data.describe().to_html(),
        'df_nombre':data.nombre_insumo,
        
        'df_stock_minimo': data.stock_minimo
        
    }
    # print(data_insumos)
    
 
    return render(request, 'insumos_reporte.html'
                  , context)
    

#Hace un conteo de los tratamientos agendados
def tratamiento_solicitado_reporte(request):
    #Estados de una Cita
    qa= TratamientoConfirmado.objects.filter(estado='Agendado')
    qc= TratamientoConfirmado.objects.filter(estado='Confirmado')
    qr= TratamientoConfirmado.objects.filter(estado='Realizado')
    qp= TratamientoConfirmado.objects.filter(estado='Pagado')
    #General
    cita= TratamientoConfirmado.objects.all().values()
    
    #DataFrame
    data_agendado= pd.DataFrame(qa,)
    
    data_confirmado= pd.DataFrame(qc,)
    data_realizado= pd.DataFrame(qr,)
    data_pagado= pd.DataFrame(qp,)
    data_pagado=pd.Series(data=qp,)
    data2= pd.DataFrame(cita, columns=['estado'],)
    data_pagado.index
    
    #Grafico en Serie de Torta
    serie= data2['estado'].value_counts()
    # serie.plot.pie(autopct='%1.1f%%')
    # plt.show()
    print(   data_pagado.index)
    # s=pd.Series(cita)
    # s.to_dict('records')
    # print("es diccionario", s)
   #Mas pruebas
    graficocita=data2.to_dict
    conteo= serie.values
    draw= serie.to_numpy().tolist()
   
    
    print("es agrupado", data2.groupby('estado'))
    
    #Graficos de prueba
    # data2.groupby('estado').plot(kind = 'bar', 
    #                              stacked = 'True',          # Muestra las barras apiladas
    #                             alpha = 0.4,               # nivel de transparencia
    #                             width = 0.9,               # Grosor de las barras para dejar espacio entre ellas
    #                             figsize=(9,4))
    # plt.xlabel('Citas')
    # plt.ylabel('Cantidad')
    # plt.show()
    
    
    total = data_agendado.loc[0]
    
    context={
     
        'df': data2.to_html,
        #Trae el conteo de Cantidades gf1
        'gf1':serie.to_frame,
        # 'df_estado': data2['estado'],
        'df_estado':data2.estado,
        #
        'list': data2.estado.to_string,
        'total_agendado': data_agendado.count() -1,
        'total_confirmado': data_confirmado.count() -1,
        'total_realizado': data_realizado.count() -1,
        'total_pagado': data_pagado.count() -1,
        'grafico': serie,
        'graficocita':graficocita, 
        'conteo': conteo,
        'draw':draw
        # 's':s,
     
        
    }
    # total=  data.head()
   
   
    return render(request, 'tratamiento_solicitado_reporte.html', context)
     

#Convierte a JSON
def cita_reporte(request):
    cita_list= TratamientoConfirmado.objects.all().values()
    
    data = []
    for cita in cita_list:
        estado_cita = cita['estado'] 
        r = lambda: random.randint(0,255)
        data.append({'value': cita['estado'], 'label': estado_cita, 'color': '#%02X%02X%02X' % (r(),r(),r())})
    
    return HttpResponse(json.dumps(data), content_type='application/json; utf-8') 

