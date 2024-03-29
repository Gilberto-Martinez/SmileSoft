# Generated by Django 3.1.13 on 2022-11-22 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cobros', '0007_auto_20221118_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='estado',
            field=models.CharField(choices=[('Emitido', 'Emitido'), ('Anulado', 'Anulado')], default='Emitido', max_length=12, verbose_name='Condición de venta'),
        ),
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id_detalle_factura', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(default=1, max_length=2)),
                ('descripcion', models.CharField(max_length=30)),
                ('precio_unitario', models.IntegerField()),
                ('exentas', models.IntegerField()),
                ('gravado_5_porc', models.IntegerField()),
                ('gravado_10_porc', models.IntegerField()),
                ('id_factura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_cobros.factura')),
            ],
            options={
                'verbose_name': 'Detalle de Factura',
                'verbose_name_plural': 'Detalles de Factura',
            },
        ),
    ]
