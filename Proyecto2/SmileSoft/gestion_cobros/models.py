from email.policy import default
from random import choices
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

    def get_id_cobro(self):
        return int(self.id_cobro_contado)

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

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    sub_nro_factura1 = models.CharField(max_length=3, null=False, blank=True)
    sub_nro_factura2 = models.CharField(max_length=3, null=False, blank=True)
    sub_nro_factura3 = models.IntegerField(null=False, blank=True)
    nro_factura = models.CharField(max_length=60, null=True, blank=True,)
    numero_documento = models.CharField(max_length=10, null=True)
    razon_social = models.CharField(max_length=60, null=True, blank=True, verbose_name='Nombre o Razón Social')
    direccion = models.CharField(max_length=80, null=True, blank=True, verbose_name='Dirección')
    fecha = models.DateField(auto_now_add=True)
    CO = 'Contado'
    CR = 'Credito'
    CONDICIONES = ((CO, 'Contado'), (CR, 'Credito'))
    condicion_venta = models.CharField(max_length=12, choices=CONDICIONES,default='Contado' ,verbose_name='Condición de venta')
    telefono = models.CharField(max_length=20, null=True, blank=True)
    total_pagar = models.IntegerField()
    iva_5 = models.FloatField(null=True)
    iva_10= models.FloatField(null=True)
    total_iva = models.FloatField(null=True)
    E = 'Emitido'
    A = 'Anulado'
    ESTADOS = ((E, 'Emitido'), (A, 'Anulado'))
    estado = models.CharField(max_length=12, choices=ESTADOS,default='Emitido' ,verbose_name='Condición de venta')

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        # ordering = ["nombre"]
        # db_table = 'DetalleCobroContado'

    def __str__(self):
        return self.id_factura


class DetalleFactura(models.Model):
    id_detalle_factura = models.AutoField(primary_key=True)
    id_factura = models.ForeignKey(
                                Factura,
                                null=True,
                                blank=True,
                                on_delete=models.PROTECT
    )
    cantidad = models.IntegerField(default=1)
    descripcion = models.CharField(max_length=40, null=False, blank=False)
    precio_unitario = models.IntegerField()
    exentas = models.IntegerField(null=True)
    gravado_5_porc = models.IntegerField(null=True)
    gravado_10_porc = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalles de Factura'
        # ordering = ["nombre"]
        # db_table = 'DetalleCobroContado'

    def __str__(self):
        return self.id_detalle_factura