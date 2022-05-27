from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *
# Register your models here.

class PersonalizadoUserAdmin(UserAdmin):
#esta es la clase que estira el CRUD DE USUARIO
    # readonly_fields = ('usuario',)
    list_filter = ('usuario','numero_documento', 'fecha_creacion')
    fieldsets = (
        (None, {'fields': ('usuario', 'numero_documento')}),
        (('Permisos'), {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        (('Roles'),{'fields':('groups',)}),
        #PARA EL CASO ESTIRAR ESTE AGREGAR CONTRASEÑA ES ESTE 
        (('Cambiar contraseña'),{'fields':('password',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('usuario', 'password1','password2', 'numero_documento'),
        }),
    )

    list_display = ["usuario", "numero_documento",
                    'is_staff', 'is_active', 'is_admin', 'fecha_creacion']
    # list_filter = ["usuario"]
    search_fields = ["usuario","numero_documento",]
    ordering = ["usuario"]
    filter_horizontal = ('groups',)


class AdminTratamiento(admin.ModelAdmin):
    list_display = ["nombre_tratamiento", "descripcion_tratamiento","precio"]
    list_filter = ["nombre_tratamiento"]
    search_fields = ["nombre_tratamiento"]










admin.site.site_header = 'Bienvenido a Smilesoft'
admin.site.site_title = 'SmileSoft'

admin.site.register(Usuario, PersonalizadoUserAdmin)