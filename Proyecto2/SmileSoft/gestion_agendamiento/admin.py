from django.contrib import admin
from .models import *
admin.site.register(Cita)

# Register your models here.
class AdminCita(admin.ModelAdmin):
    inlines = [Cita]
    list_display = ["id_cita","numero_documento"]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('numero_documento',),
        }),
    )

    fieldsets = (
        (None, {'fields': ('numero_documento',)}),
    )

 

    # list_display = ["nombre", "apellido",]
    # list_filter = ['numero_documento']
    list_display_links = ['numero_documento',]
    search_fields = ['numero_documento', ]
    ordering = ['numero_documento']