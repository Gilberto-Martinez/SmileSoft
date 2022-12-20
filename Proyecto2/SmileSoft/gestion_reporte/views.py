import array
import datetime
from http.client import HTTPResponse
from macpath import join
from time import strftime
from xmlrpc.client import _datetime
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
from gestion_cobros.models import CobroContado, Factura
from django.db.models import Sum
from django.db.models import Count    
from collections import Counter
import numpy as np
from datetime import date

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
        data = {}
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
        context['title'] = 'Reporte de Ingresos'
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
        
        data= pd.DataFrame(solicitado, columns=["Lista de Mas Solicitados"])
        
        
        
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
   
    
    tabla=pd.DataFrame(resultado, index=['Cantidades'])
    # t_valores= tabla.tolist()

    data_cantidades= pd.DataFrame(resultado, index=[0])
    
    columnas= data_cantidades.columns
    #Son los tratamientos
    indices= columnas.to_numpy().tolist()
    print("es columnas", columnas,"\n Es indice", indices)
    
    cantidades= np.array(data_cantidades)
 
    vector=cantidades.tolist()
    
    #Se debe concatenar la lista para mostrar en el grafico y con li, se logra suprimir un corchete 
    li=str(vector)[1:-1] 
    print("es lista",type(lista_cantidades), "Imprime,",li, type(li))
    es_maximot=max(vector)
    print("es vector", vector, "es del tipo", type(vector), "es maximo t", es_maximot)
    
    #Conversiones a Lista, y son las cantidades
    grafico= data_cantidades.to_numpy().tolist()
    
    valores= data_cantidades.values
    
    valores_grafico=valores.tolist()

    #draw= data_cantidades.to_dict()
    print("es grafico", type(grafico), "son valores", valores, "son los valores", valores_grafico, type(valores_grafico))
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
                'data_cantidades':data_cantidades,
                'columnas': columnas,
                'indices':indices, 
                'valores_grafico': valores_grafico,
                'li':li,
                'tabla': tabla.to_html, 
               
                
                
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
  
    # grupo= data_agendado.groupby(data_agendado.index.month).tail(1).reset_index()
    
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
        # 'grupo':grupo,
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



def retorna_total_vendido(request):
    total = CobroContado.objects.all().aggregate(Sum('monto_total'))['monto_total__sum']
    if request.method == "GET":
        return JsonResponse({'total': total})


#ES  DE COBRO CONTADO
# def reporte_ingresos(request):
#     #Estados de una Cita
#     qa= TratamientoConfirmado.objects.filter(estado='Agendado')
#     qr= TratamientoConfirmado.objects.filter(estado='Realizado')
#     qc= TratamientoConfirmado.objects.filter(estado='Confirmado')
#     qp= TratamientoConfirmado.objects.filter(estado='Pagado')
#     #General
#     cita= TratamientoConfirmado.objects.all().values()
    
#     #Ingresos
#     tabla_ingresos=CobroContado.objects.all().values()
#     data= CobroContado.objects.all().values()
#     df = pd.DataFrame(data)
#     df[['fecha', 'monto_total']]
#     monto= df[['monto_total']]
#     fecha_mes= df[['fecha']]
#     suma_monto=monto.sum()

#     # es_fecha=df.reset_index(col_level='fecha')
#     # mes=df['fecha'].dt.month
#     # print("Es la fecha la columna", es_fecha)
#     # print("es el mes ", mes)
    
    
#     data_fecha= pd.DataFrame(data, columns=['fecha',])
#     # Trae un datafraem como entre corchete de las fechas (mes)
#     mes =data_fecha.set_index("fecha")
    
#     print(" ES FECHA", mes, "del tipo", type(mes))
    
#     # data_fecha=  data_fecha.set_index("index","fecha")
#     # # data_fecha["Month"]= data_fecha.dt.month
#     # data_fecha.head()
    
#     # print( "####ES DATA FECHA############",data_fecha )
#     # serie_meses=pd.Series(data)
#     # lista_fecha= serie_meses.dt.month
#     # print (" es lista de meses", lista_fecha)
    
#     # monto_mes= datetime(date(df[['fecha']])).month== 10
#     # # filterdate = datetime.date(input())
#     # d1 = d1[(d1['New_Date'] > '{filterdate}') & (d1['New_Date'] != 'NaT')]
#     # date_fecha= date(fecha_mes['fecha']).month==10
#     # es_mes = date(fecha_mes).month==10
    
#     # print ("esto muestra", es_mes)
  
    
#     # print("es la tabla cobro", df)
#     #DataFrame
#     tabla=pd.Series(tabla_ingresos)
#     data_agendado= pd.DataFrame(qa, columns=['Agendado'])
#     data_realizado= pd.DataFrame(qr, columns=['Realizado'])
#     print ("es del tipo la Tabla..... ", type(tabla))
    
#     # grupo= data_agendado.groupby(data_agendado.index.month).tail(1).reset_index()
    
#     data_confirmado= pd.DataFrame(qc,)
#     data_pagado= pd.DataFrame(qp,)
#     data_pagado=pd.Series(data=qp,)
#     data2= pd.DataFrame(cita, columns=['estado'], )
#     data_pagado.index
    
#     #Grafico en Serie de Torta
#     serie= data2['estado'].value_counts()
#     # serie.plot.pie(autopct='%1.1f%%')
#     # plt.show()
#     print(   data_pagado.index)
#     # s=pd.Series(cita)
#     # s.to_dict('records')
#     # print("es diccionario", s)
#    #Mas pruebas
#     graficocita=data2.to_dict
#     conteo= serie.values
#     draw= serie.to_numpy().tolist()
   
    
    
#     context={
#         # 'tabla':tabla,
#         'df': data2.to_html,
#         #Trae el conteo de Cantidades gf1
#         'gf1':serie.to_frame,
#         # 'df_estado': data2['estado'],
#         'df_estado':data2.estado,
#         #
#         'list': data2.estado.to_string,
#         'total_agendado': data_agendado.count().values,
#         'total_realizado': data_realizado.count().values,
#         'total_confirmado': data_confirmado.count() -1,
#         'total_pagado': data_pagado.count() -1,
#         'grafico': serie,
#         'graficocita':graficocita, 
#         'conteo': conteo,
#         'draw':draw,
#         'tabla':tabla,
#         'df':df[['fecha', 'monto_total']].to_html,
#         'monto': monto.to_html,
#         'suma_monto': suma_monto, 
#         'mes':mes,
#         # 'data_fecha': data_fecha,
#         # 'monto_mes': monto_mes, 
     
#         # 'grupo':grupo,
#         # 'draw2':draw2,
#         # 's':s,
     
        
#     }
#     # total=  data.head()
   
   
#     return render(request, 'reporte_ingresos.html', context)



def reporte_ingresos(request):
    #Estados de una Cita
    qa= TratamientoConfirmado.objects.filter(estado='Agendado')
    qr= TratamientoConfirmado.objects.filter(estado='Realizado')
    qc= TratamientoConfirmado.objects.filter(estado='Confirmado')
    qp= TratamientoConfirmado.objects.filter(estado='Pagado')
    #General
    cita= TratamientoConfirmado.objects.all().values()
    
    #Ingresos
    tabla_ingresos=CobroContado.objects.all().values()
    
    #Tabla de Ingresos y Montos en General
    
    data= Factura.objects.all().values()
    df = pd.DataFrame(data)
    df[['fecha', 'total_pagar']]
    tabla_factura = pd.DataFrame(data, columns=['fecha','total_pagar'])
    tabla_factura_renombrada = tabla_factura.rename({'fecha':'Mes', 'total_pagar': 'total'}, axis=1)
    tabla_renombrada= tabla_factura.rename({'fecha': 'Fecha', 'total_pagar': 'Monto'}, axis=1)
    # print("||||||||||||||||||||", tabla_renombrada)
    data_fecha= pd.DataFrame(data, columns=['fecha'])
    
    '''Trae el monto por mes'''
    
    tabla_mes_monto=  df[['fecha', 'total_pagar']]
    
    tabla_mensual= tabla_mes_monto.groupby(['fecha']).agg({"total_pagar":sum})
    tabla_mensual_renombrada= tabla_mensual.rename({'fecha': 'Fecha', 'total_pagar': 'Monto'}, axis=1)
    

    
    fecha_factura=pd.to_datetime(tabla_factura_renombrada['Mes'])# trae solo la columna fecha
    '''Trae el nro del mes'''
    numero_mes= fecha_factura.dt.month #trae el numero del mes 
    

    '''POR MES'''
    mes_monto= fecha_factura.drop_duplicates().groupby(numero_mes).count()
    print("es general", mes_monto)
    
    monto= df[['total_pagar']]
    
    # general=  tabla_mensual_renombrada.drop_duplicates().groupby('fecha').count()
    # general['Total por año'] = general['Monto'].sum()
    
    '''Funcion que sumara por mes'''
    '''EXTRAER MONTOS MENSUALES'''
    tabla_monto=  df[['fecha']]
    tabla_monto_renombrada= tabla_monto.rename({'fecha':'MES'})
    general=tabla_monto_renombrada.drop_duplicates().groupby(numero_mes).count()
    
    
    general['Gs']= tabla_mensual_renombrada['Monto'].sum()
    tabla_fecha= pd.DataFrame(general, columns=['Mes'])
    
    
    
    
    print("ES FECHA", tabla_fecha)
    
    tabla_general=tabla_mes_monto.drop_duplicates().groupby(numero_mes).count()
    
    tabla_general=general.set_index('Gs')
    
    print('es TABLA GENERAL ||||||', tabla_general, '|||||||||')
    


    '''Sale los totales por mes'''
    monto_por_mes= tabla_mes_monto.groupby(numero_mes==11).sum()
  
    
    monto_por_mes_renombrada= monto_por_mes.rename({'total_pagar': 'Gs'}, axis=1)
    guaranies=monto_por_mes_renombrada.set_index('Gs')# trae la columna de totales por mes
    
    monto_por_mes_renombrada=monto_por_mes_renombrada.set_index('Gs')# trae la columna de totales por mes
    '''INSERTA UNA NUEVA COLUMNA'''
    nombre_de_meses= ['Noviembre', 'Diciembre']
    nueva_tabla= monto_por_mes_renombrada.insert(loc= 0, column= 'Meses',value=nombre_de_meses)
    
    
    '''SERA EL GRAFICO'''
    # grafico_mes= monto_por_mes_renombrada['Gs'].values

    # mes_grafico=monto_por_mes_renombrada['Gs'].value_counts()

   
    # draw= grafico_mes.to_numpy().tolist()
    
    
    '''Sera la tabla ingresos'''
    
    '''INGRESOS'''
  
    
    
    data_mes= pd.DataFrame(monto_por_mes, index=[1])
    
    
    # data_monto
    
    print('°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°',data_mes, '°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°')
    # tabla_monto_por_mes=monto_por_mes.groupby('fecha').total_pagar.sum()
    #general[numero_mes] = general['total_pagar'].sum() 
    
    
    print("es tabla", general)
    
    '''Trae la cantidad por mes'''
    grupo_factura= tabla_factura.drop_duplicates().groupby('fecha').count()
    # fecha_factura.loc['Total por mes'] =  grupo_factura['total_pagar'].sum()
  
    
  
    
    print("es fecha factura", fecha_factura, "es mes", numero_mes)
    
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print(nuevo)
    mes_factura= lambda x:x[:7]
    
    print("es mes_factura", mes_factura)
    # tabla_factura["fechaMes"]= tabla_factura[['fecha']].astype(str).map(mes_factura)
    
    '''Por mes'''
    
    mes_numero= tabla_factura[['fecha']]
    print("es mes", mes_numero)
        
    # tabla_factura['month']= tabla_factura.dt.strftime('%m')
    tabla_mes=pd.to_datetime(df['fecha']).dt.to_period('D') #solo trae el dia con el año
    
    
    print('es tabla mes', tabla_mes)
    '''Es una tabla que indica el Grupo por dia del Mes'''
    grupo_mes= data_fecha.drop_duplicates().groupby('fecha').count()
    
   
    print("es grupo", grupo_mes)
    '''Hace un conteo por dias de las Facturas'''
    grupo= tabla_factura.drop_duplicates().groupby('fecha').count()
    grupo.loc['Total por año'] = grupo['total_pagar'].sum()
    
    grupo_renombrado= grupo.rename({'fecha': 'Fecha', 'total_pagar': 'Cantidad'}, axis=1)
    
    
    
    
    
    
    
    # data_factura= pd.DataFrame({'Lista de Fechas': pd.to_datetime(data_fecha, format='%Y/%m/%d')})
    
    # data_factura= pd.DataFrame({'Lista de Fechas': data_fecha.stack().unstack()})
   
    # data_factura= pd.DataFrame({'Lista de Fechas': pd.to_datetime(data_fecha, ).dt.month})
    
    # df['Lista de Fechas']= pd.to_datetime(df['Lista de Fechas']) 

    
    # df['Month'] = data_factura['Lista de Fechas'].dt.month == 12
    # print(df)
    
    # print("es datafactura", data_factura)
    
    
    
 
    # monto= df[['total_pagar']]
    
    grupo_monto= tabla_factura
    grupo_monto_renombrado= tabla_factura.rename({'fecha': 'Fecha', 'total_pagar': 'Monto en Gs'}, axis=1)
    grupo_monto['Total por dia'] = grupo_monto['total_pagar'].sum()
    
  
  
    fecha_mes= df[['fecha']]
    suma_monto=monto.sum()
    suma= suma_monto.rename({'total_pagar': ''}, axis=1)
    caja= suma.values

    # es_fecha=df.reset_index(col_level='fecha')
    # mes=df['fecha'].dt.month
    # print("Es la fecha la columna", es_fecha)
    # print("es el mes ", mes)
    
    
    data_fecha= pd.DataFrame(data, columns=['fecha',])
    # Trae un datafraem como entre corchete de las fechas (mes)
    mes =data_fecha.set_index("fecha")
    
    print(" ES FECHA", mes, "del tipo", type(mes))
    
    # data_fecha=  data_fecha.set_index("index","fecha")
    # # data_fecha["Month"]= data_fecha.dt.month
    # data_fecha.head()
    
    # print( "####ES DATA FECHA############",data_fecha )
    # serie_meses=pd.Series(data)
    # lista_fecha= serie_meses.dt.month
    # print (" es lista de meses", lista_fecha)
    
    # monto_mes= datetime(date(df[['fecha']])).month== 10
    # # filterdate = datetime.date(input())
    # d1 = d1[(d1['New_Date'] > '{filterdate}') & (d1['New_Date'] != 'NaT')]
    # date_fecha= date(fecha_mes['fecha']).month==10
    # es_mes = date(fecha_mes).month==10
    
    # print ("esto muestra", es_mes)
  
    
    # print("es la tabla cobro", df)
    #DataFrame
    tabla=pd.Series(tabla_ingresos)
    data_agendado= pd.DataFrame(qa, columns=['Agendado'])
    data_realizado= pd.DataFrame(qr, columns=['Realizado'])
    print ("es del tipo la Tabla..... ", type(tabla))
    
    # grupo= data_agendado.groupby(data_agendado.index.month).tail(1).reset_index()
    
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
    # graficocita=data2.to_dict
    # conteo= serie.values
    # draw= serie.to_numpy().tolist()
   
    
    
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
        # 'draw':draw,
        'tabla':tabla,
        'df':df[['fecha', 'total_pagar']].to_html,
        'tabla_renombrada':tabla_renombrada.to_html,
        'monto': monto.to_html,
        'tabla_monto_renombrada':tabla_monto_renombrada.to_html,
        'suma_monto': suma_monto, 
        'suma':suma,
        'caja': caja,
        'mes':mes,
        'grupo_mes': grupo_mes.to_html,
        'grupo':grupo.to_html,
        'grupo_renombrado': grupo_renombrado.to_html,
        'grupo_monto':grupo_monto.to_html,
        'grupo_monto_renombrado':grupo_monto_renombrado.to_html,
        'tabla_mes':tabla_mes.to_frame(),
        'numero_mes': numero_mes,
        'grupo_factura':grupo_factura.to_html,
        'tabla_mensual':tabla_mensual.to_html,
        'tabla_mensual_renombrada':tabla_mensual_renombrada.to_html,
        'general': general.to_html,
        'tabla_general':tabla_general.to_html,
        'tabla_mes': tabla_mes.to_frame,
        'monto_por_mes':monto_por_mes.to_html,
        'monto_por_mes_renombrada':monto_por_mes_renombrada.to_html,
        # 'grafico_mes': grafico_mes,
        'nueva_tabla': nueva_tabla,
        'data_mes':data_mes.to_html,
        'guaranies': guaranies.to_html, 
        # 'data_mes': data_mes.to_html,
        # 'ingreso_tabla':ingreso_tabla,
        
        # 'draw2':draw2,
        # 's':s,
     
        
    }
    # total=  data.head()

    return render(request, 'reporte_ingresos.html', context)