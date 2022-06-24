from django.db import models
from gestion_tratamiento.models import Tratamiento
from gestion_administrativo.models import Paciente
# Create your models here.

class Cita(models.Model):
    id_cita=models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tratamiento_solicitado=models.OneToOneField(
                                                Tratamiento,
                                                max_length=45,
                                                null=False,
                                                blank= False,
                                                on_delete=models.PROTECT,
                                                verbose_name='Motivo de consulta'
    )
    # start_time=models.DateField()
    # end_time=models.DateField()
    
    fecha = models.DateField()
    
    hora = models.TimeField()
    
    class Meta(object):
        verbose_name_plural = 'Cita'
        
     

    def __str__(self):
        return str(self.paciente)
