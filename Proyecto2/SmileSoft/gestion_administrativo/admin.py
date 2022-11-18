from django.contrib import admin
from .models import *
#from .forms import *

# Register your models here.


class AdminEmpresa(admin.ModelAdmin):
    #add_form_template = PersonForm
    fieldsets = (
        (None, {'fields': (
            'ruc',)}),
        (('Datos de la Empresa'), {'fields': (
            'nombre_empresa',
            'correo_electronico',
            'direccion',
            'telefono',
            'timbrado',
            'f_inicio_vigencia',
            'f_fin_vigencia'
            
        )
        }
        ),
    )
   

class AdminPersona(admin.ModelAdmin):
    #add_form_template = PersonForm
    fieldsets = (
        (None, {'fields': (
                            'numero_documento',)}),
        (('Informacion Personal'), {'fields': (
                                            'nombre', 
                                            'apellido', 
                                            'correo_electronico', 
                                            'direccion', 
                                            'telefono',
                                            'fecha_nacimiento',
                                            'sexo',
                                        )
                                    }
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre', 'apellido',),
        }),
    )

    list_display = ['numero_documento',"nombre", "apellido","es_funcionario","es_paciente", "es_especialista_salud"]
    # list_filter = ['numero_documento']
    search_fields = ["numero_documento","nombre","apellido",]
    ordering = ["nombre","apellido",]
    # filter_horizontal = ('groups',)

class FuncionarioCargoInline(admin.TabularInline):
    model = FuncionarioCargo
    extra = 1
    # autocomplete_fields = ['cargo',]

class AdminFuncionarioCargo(admin.ModelAdmin):
    inlines = [FuncionarioCargoInline,]
    search_fields = ['nombre']
    ordering = ['nombre']

class AdminFuncionario(admin.ModelAdmin):
    inlines = [FuncionarioCargoInline,]
    list_display = ["id_funcionario","numero_documento"]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('numero_documento',),
        }),
    )

    fieldsets = (
        (None, {'fields': ('numero_documento',)}),
    )

    filter_horizontal = ['cargos']

    # list_display = ["nombre", "apellido",]
    # list_filter = ['numero_documento']
    list_display_links = ['numero_documento',]
    search_fields = ['numero_documento_nombre', ]
    # ordering = ['numero_documento']

# class EspecialistaSaludEspInline(admin.TabularInline):
#     model = TrabajoRealizado
#     extra = 1
    #autocomplete_fields = ['especialidad',]

class AdminEspecialistaSaludEsp(admin.ModelAdmin):
    # inlines = [EspecialistaSaludEspInline,]
    search_fields = ['categoria']
    #ordering = ['categoria']


# class AdminEspecialistaSalud(admin.ModelAdmin):
#     # inlines = [EspecialistaSaludEspInline,]
#     fieldsets = (
#         (None, {'fields': ('numero_documento',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('numero_documento',),
#         }),
#     )
#     # list_display = ["nombre", "apellido",]
#     # list_filter = ['numero_documento']
#     search_fields = ['numero_documento', 'id_especialista_salud','numero_documento_name', 'id_especialista_salud_name']
#     # search_fields = ['foreign_key__related_fieldname']
#     ordering = ['numero_documento']

class AdminProveedor(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('numero_documento',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('numero_documento',),
        }),
    )
    # list_display = ["nombre", "apellido",]
    # list_filter = ['numero_documento']
    search_fields = ['numero_documento',]
    ordering = ['numero_documento']

# class TratamientoRealizadoInline(admin.TabularInline):
#     model = TratamientoRealizado
#     extra = 1
    # autocomplete_fields = ['cargo',]

# class AdminTratamientoRealizado(admin.ModelAdmin):
#     inlines = [TratamientoRealizadoInline,]
#     search_fields = ['codigo_tratamiento']
#     ordering = ['codigo_tratamiento']

# class AdminPaciente(admin.ModelAdmin):
#     inlines = [TratamientoRealizadoInline,]
#     # list_filter = ('numero_documento',)
#     fieldsets = (
#         (None, {'fields': (
#                             'numero_documento', 
#                             'grupo_sanguineo',
#                             )}),
#         (('Antecedente Clínico'), {'fields': (
#                                             'enfermedad_base', 
#                                             'alergia', 
#                                             'intolerancia_anestecia', 
#                                             'frecuencia_higiene_bucal',
#                                             'cirugias',
#                                             'afeccion_cronica_familiar',
#                                             'medicamento',
#                                             'caries',
#                                         )
#                                     }
#         ),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             # 'fields': ('numero_documento','numero_ficha'),
#             'fields': ('numero_documento'),
#         }),
#     )

#     # list_display = ["nombre", "apellido",]
#     # list_filter = ['numero_documento']
#     search_fields = ['numero_documento',]
#     ordering = ['numero_documento']
class AdminPaciente(admin.ModelAdmin):
    search_fields = ['numero_documento_nombre',]
    

class AdminEspecialistaSalud(admin.ModelAdmin):
    search_fields = ['numero_documento', 'id_especialista_salud_nombre']

    
admin.site.site_header = 'Bienvenido a Smilesoft'
admin.site.site_title = 'SmileSoft'

admin.site.register(Empresa, AdminEmpresa)
admin.site.register(Persona, AdminPersona)
admin.site.register(Cargo, AdminFuncionarioCargo)
# admin.site.register(Categoria, AdminEspecialistaSaludEsp)
admin.site.register(Funcionario, AdminFuncionario)
admin.site.register(Proveedor)
admin.site.register(Paciente)#, AdminPaciente)
admin.site.register(EspecialistaSalud, AdminEspecialistaSalud)
# admin.site.register(Insumo)
admin.site.register(PacienteTratamientoAsignado)
admin.site.register(Especialidad)
