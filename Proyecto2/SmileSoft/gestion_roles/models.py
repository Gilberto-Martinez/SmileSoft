from django.db import models
from agregar_mas.models import *
from django.contrib.auth.models import Group, Permission,GroupManager
# Create your models here.

# class Rol(Group):
#     nombre = models.CharField(('name'), max_length=150, unique=True)
#     permiso = models.ManyToManyField(Permission,verbose_name=('permisos'),blank=True,)
#     fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)    
#     objects = GroupManager()
    
    
#     class Meta:
#             verbose_name = ('rol')
#             verbose_name_plural = ('roles')
#             db_table= 'Rol'

#     def __str__(self):
#         return self.nombre

#     def natural_key(self):
#         return (self.nombre,)