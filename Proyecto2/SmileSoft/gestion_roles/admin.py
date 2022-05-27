from os import name
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from .forms import *
from .models import *

class PersonalizadoGroupAdmin(GroupAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)



# Register your models here.
admin.site.site_header = 'Bienvenido a Smilesoft'
admin.site.site_title = 'SmileSoft'

# admin.site.register(Rol, PersonalizadoGroupAdmin)