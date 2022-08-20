from django.db import models
from gestion_tratamiento.models import Tratamiento
from gestion_administrativo.models import Paciente

class CobroContado(models.Model):
    id_cobro_contado = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(
                                Paciente,
                                null=True,
                                blank=True,
                                on_delete=models.PROTECT
    )
    numero_documento = models.CharField(max_length=10, verbose_name='numero de documento')
    razon_social = models.CharField(max_length=100, verbose_name='Nombre o razón social')
    fecha = models.DateField(auto_now_add=True)
    monto_total = models.BigIntegerField()
    class Meta:
        verbose_name = 'Cobro al contado'
        verbose_name_plural = 'Cobros al contado'
        # ordering = ["nombre"]
        db_table = 'CobroContado'

    def __str__(self):
        return self.id_cobro_contado

    def get_fecha(self):
        return self.fecha

class DetalleCobroContado(models.Model):
    cobro = models.ForeignKey(
                                CobroContado,
                                null=False,
                                blank=False,
                                on_delete=models.PROTECT
    )
    tratamientos = models.ManyToManyField(
                                                Tratamiento,
                                                through='DetalleCobroTratamiento',
                                                related_name='detalle_set',
                                                # null=True,
                                                # blank=True
    )

    class Meta:
        verbose_name = 'Detalle de cobro al contado'
        verbose_name_plural = 'Detalles de cobros al contado'
        # ordering = ["nombre"]
        db_table = 'DetalleCobroContado'

    def __str__(self):
        return self.cobro


class DetalleCobroTratamiento(models.Model):
    detalle_cobro = models.ForeignKey(
                                        DetalleCobroContado,
                                        # null=False,
                                        # blank=False,
                                        on_delete=models.CASCADE
    )
    tratamiento = models.ForeignKey(
                                    Tratamiento,
                                    # null=False,
                                    # blank=False,
                                    on_delete=models.CASCADE
    )