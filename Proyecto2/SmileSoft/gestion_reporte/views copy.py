from django.shortcuts import render
from django.views.generic import  TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from gestion_agendamiento.models import Cita
from gestion_reporte.form import ReporteTratamientoForm
# Create your views here.
class ReporteTratamientoView(TemplateView):
    template_name = 'reporte_tratamiento.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
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
                        # format(s.subtotal, '.2f'),
                        # format(s.iva, '.2f'),
                        # format(s.total, '.2f'),
                    ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
       
        return JsonResponse(data, safe=False)
        # return render(request, "reporte_tratamiento.html", data, safe=False)
   # <!-->
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte'
        context['entity'] = 'Reportes'
        # context['list_url'] = reverse_lazy('reporte_tratamiento')
        context['form'] = ReporteTratamientoForm()
        return context

def reporte(request):
    return render (request, "reporte.html")