import datetime
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
from gestion_tratamiento.models import Tratamiento
from gestion_reporte.utils import render_to_pdf
from gestion_inventario_insumos.models import Insumo
from gestion_administrativo.models import TratamientoConfirmado
from gestion_agendamiento.models import Cita
from gestion_reporte.form import ReporteTratamientoForm
    
from django.db.models import Count    
from collections import Counter
import numpy as np

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

def cantidad_veces (lista, x): 
    count = 0
    for elemento in lista: 
        if (elemento == x): 
            count = count + 1
    return count 


def tratamiento_mas_solicitado(request):
    
    qr= TratamientoConfirmado.objects.all().values()
    # data_realizado= pd.DataFrame(qr, columns=['Realizado'])
    data_realizado= pd.DataFrame(qr, )
    
    minimo= min(data_realizado)
    maximo= max(data_realizado)
    
    listado_tratamientos = TratamientoConfirmado.objects.filter(estado='Realizado')
    solicitado = []
    repeticiones = {}
    # repeticiones = dict((i, listado_tratamientos.count(i)-1) for i in listado_tratamientos if listado_tratamientos.count(i)>1)

    
    for tratamiento in listado_tratamientos:
        
        cod_tratamiento = tratamiento.get_tratamiento()
        
        tratamiento_elegido = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
        mas= tratamiento_elegido.nombre_tratamiento
        solicitado.append(mas)
        
        data= pd.DataFrame(solicitado, columns=["Tratamientos Mas Solicitados"])
        
        #Convierte el Dataframe en lista
        lista= data.to_numpy().tolist()
        
        
        conteo= Counter(solicitado)
    #Aqui hace el conteo por Cantidad de los tratamientos    
    resultado={}
    for clave in conteo:  
        valor=conteo[clave]
        if valor != 1:
            resultado[clave] = valor
            print(resultado)
            
    lista_cantidades= resultado.values
    
    data_cantidades= pd.DataFrame(resultado, index=[0])
    cantidades= np.array(data_cantidades)
    
    grafico= data_cantidades.to_numpy()
    draw= cantidades.tolist
    
    g1= grafico.tolist
    
    print("Es tipo", "#Cantidad",type(cantidades), "#draw", type(draw), )
   
    # mayor=lista.count(tratamiento)
        
        # count = 0
        # for solicitado in lista: 
        #     if (solicitado == tratamiento): 
        #         count = count + 1
        #         print("entra aqui", count)
        #cantidad_veces= lista.count(tratamiento)    
        # if lista.count(tratamiento)  > 1:
        #     repeticiones[tratamiento]= lista.count(tratamiento)-1
        #     print("Aqui", repeticiones[tratamiento])
        
            # es_mayor= max(data)
        
   
    # print( "es cantidad", lista, count)
     

     
        
    context= {
                'realizado': data_realizado.to_html,
            
                'solicitado': solicitado,
                'max':max,
                'data':data.to_html,
                'mas':mas,
                # 'mayor':mayor,
                # 'es_mayor':es_mayor,
                # 'repeticiones':repeticiones,
                'listado_tratamientos': listado_tratamientos,
                # 'cantidad_veces': cantidad_veces,
                'lista': lista,
                'resultado': resultado,
                'lista_cantidades': lista_cantidades, 
                'cantidades':cantidades,
                'grafico':grafico,
                'draw':draw,
                'g1':g1,
                
                
    }
    # for n in lista:
    #     if lista.count(n) != 1:
    #         if n in repeticiones :
    #             repeticiones[n] += 1
    #         else:
    #             repeticiones[n] = 0
    # print("Se repite",repeticiones)
       
  
        
    return render(request, "tratamiento_mas_solicitado.html", context)


# def tratamiento_mas_solicitado(request):
#     solicitado= TratamientoConfirmado.objects.filter(estado="Realizado")
#     lista_solicidados=[]
    
#     for lista in solicitado:
#         cod_tratamiento = lista.get_tratamiento()
        
        
    
#     lista_solicidados.append(cod_tratamiento)
        
#     print("es lista", {'lista_solicidados': lista_solicidados})
        
#     return render(request, "tratamiento_mas_solicitado.html",{'lista_solicidados.': lista_solicidados})

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
def reporte_cita(request):
    #Estados de una Cita
    qa= TratamientoConfirmado.objects.filter(estado='Agendado')
    qr= TratamientoConfirmado.objects.filter(estado='Realizado')
    qc= TratamientoConfirmado.objects.filter(estado='Confirmado')
    qp= TratamientoConfirmado.objects.filter(estado='Pagado')
    #General
    cita= TratamientoConfirmado.objects.all().values()
    tabla_cita=TratamientoConfirmado.objects.all()
    
    #DataFrame
    # tabla=pd.DataFrame(tabla_cita)
    data_agendado= pd.DataFrame(qa, columns=['Agendado'])
    data_realizado= pd.DataFrame(qr, columns=['Realizado'])
  
    
    
    data_confirmado= pd.DataFrame(qc,)
    data_pagado= pd.DataFrame(qp,)
    data_pagado=pd.Series(data=qp,)
    data2= pd.DataFrame(cita, columns=['estado'], )
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
    
    
    print("es tipo", type(draw))
    
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
    
    
    #Quita el Porcentaje de cada cita
    porcentaje=(serie / serie. sum()) * 100
    # draw2=porcentaje.to_numpy.to_list()
    
    context={
        # 'tabla':tabla,
        'df': data2.to_html,
        #Trae el conteo de Cantidades gf1
        'gf1':serie.to_frame,
        # 'df_estado': data2['estado'],
        'df_estado':data2.estado,
        #
        'list': data2.estado.to_string,
        'total_agendado': data_agendado.count().values,
        'total_realizado': data_realizado.count().values,
        'total_confirmado': data_confirmado.count() -1,
        'total_pagado': data_pagado.count() -1,
        'grafico': serie,
        'graficocita':graficocita, 
        'conteo': conteo,
        'draw':draw,
        'porcentaje':porcentaje,
        # 'draw2':draw2,
        # 's':s,
     
        
    }
    # total=  data.head()
   
   
    return render(request, 'reporte_cita.html', context)
     



def pdf_reporte_cita(request):
    cita= TratamientoConfirmado.objects.all().values()
    data2= pd.DataFrame(cita, columns=['estado'],)
    
    #Grafico en Serie de Torta
    # serie= data2['estado'].value_counts()
    serie= data2['estado'].value_counts()
    draw= serie.to_numpy().tolist()
    #Quita el Porcentaje de todos de cada cita
    porcentaje=(serie / serie. sum()) * 100
    #Muestra en Lista
    tporcentaje=porcentaje.values
    fecha_actual= (datetime.datetime.now().strftime('%d/%m/%Y'))
    # Porcentaje individual
      # Filtro
    qa= TratamientoConfirmado.objects.filter(estado='Agendado')
    qr= TratamientoConfirmado.objects.filter(estado='Realizado')
      #DataFrame
    data_agendado= pd.DataFrame(qa, columns=['Agendado'])
    data_realizado= pd.DataFrame(qr, columns=['Realizado'])
    #
    A_porcentaje=(data_agendado/ data_agendado. sum()) * 100
    
  
    
    context={
         'draw':draw,
         'gf1':serie.to_frame,
         'porcentaje':porcentaje,
         'df': tporcentaje,
         'fecha_actual': fecha_actual,
         
        'total_agendado': A_porcentaje,
        'total_realizado': data_realizado.count().values,
         
         
    }
 
    pdf = render_to_pdf("pdf_reporte_cita.html", context)
    
    return HttpResponse(pdf, content_type='application/pdf')

#Apuntes de un DATAFRAME
def apuntes_graficos(request):
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
   
   
    return render(request, 'apuntes_graficos.html', context)

#Convierte a JSON
def cita_reporte(request):
    cita_list= TratamientoConfirmado.objects.all().values()
    
    data = []
    for cita in cita_list:
        estado_cita = cita['estado'] 
        r = lambda: random.randint(0,255)
        data.append({'value': cita['estado'], 'label': estado_cita, 'color': '#%02X%02X%02X' % (r(),r(),r())})
    
    return HttpResponse(json.dumps(data), content_type='application/json; utf-8') 

