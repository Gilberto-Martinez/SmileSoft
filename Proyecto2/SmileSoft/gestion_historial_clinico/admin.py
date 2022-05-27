from django.contrib import admin
from .models import *
#from .forms import *
# class AdminAntecedenteClinico(admin.ModelAdmin):
#     readonly_fields = ('id_antecedente',)
#     fieldsets = (
#             (None, {'fields': (
#                             'id_antecedente',)}),
#         (('Antecedente Clínico del Paciente'), {'fields': (
#                                             'enfermedad_base',
#                                             'alergia', 
#                                             'tolerancia_anestecia', 
#                                             'frecuencia_higiene_bucal', 
#                                             'medicamento',
#                                             'cirugias',
#                                             'caries',
#                                             'grupo_sanguineo'
#                                         )
#                                     }
#         ),
#         (('Antecedente Clinico Familiar'), {'fields': (
#                                             'afeccion_cronica_familiar',
#                                             'afecciones_graves',
#                                         )
#                                     }
#         ),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('grupo_sanguineo', 'alergia',),
#         }),
#     )

#     list_display = ["grupo_sanguineo", "alergia",]
#     #list_filter = ['numero_documento']
#     #search_fields = ['numero_documento',]
#     #ordering = ['numero_documento']
#     # filter_horizontal = ('groups',)


admin.site.site_header = 'Bienvenido a Smilesoft'
admin.site.site_title = 'SmileSoft'
# Register your models here.
#admin.site.register(AntecedenteClinico, AdminAntecedenteClinico)
admin.site.register(HistorialClinico)