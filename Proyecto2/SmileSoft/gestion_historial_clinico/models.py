from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.fields.related import ForeignKey
from django.template.defaultfilters import default
from gestion_administrativo.models import EspecialistaSalud
from gestion_administrativo.models import Paciente
from gestion_tratamiento.models import Tratamiento

class HistorialClinico(models.Model):
    id_historial_clinico = models.AutoField(primary_key=True)
    tratamiento = models.ForeignKey(
                                    Tratamiento, 
                                    null=False, 
                                    blank=False, 
                                    on_delete=models.PROTECT,
                                    verbose_name='Código de tratamiento'
                                )
    paciente = models.ForeignKey(
                                    Paciente, 
                                    null=False, 
                                    blank=False, 
                                    on_delete=models.PROTECT,
                                    verbose_name='Id de historial clinico'
                                )
    especialista = models.ForeignKey(
                                    EspecialistaSalud,
                                    on_delete=models.PROTECT,
                                    blank=False,
                                    null=True,
    )
    fecha_realizacion = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Tratamientos Realizados'
        db_table = 'HistorialClinico'

    def __str__(self):
        return str(self.id_historial_clinico)