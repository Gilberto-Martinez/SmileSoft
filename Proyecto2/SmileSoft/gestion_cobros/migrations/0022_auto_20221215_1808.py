# Generated by Django 3.1.13 on 2022-12-15 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cobros', '0021_auto_20221209_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComprobanteGasto',
            fields=[
                ('id_comprobante', models.AutoField(primary_key=True, serialize=False)),
                ('numero_comprobante', models.CharField(max_length=25)),
                ('total_monto', models.BigIntegerField()),
                ('condicion_venta', models.CharField(choices=[('Contado', 'Contado'), ('Credito', 'Credito')], default='Contado', max_length=12, verbose_name='Condición de venta')),
                ('fecha', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Comprobante de Gasto',
                'verbose_name_plural': 'Comprobantes de gastos',
            },
        ),
        migrations.CreateModel(
            name='Gasto',
            fields=[
                ('id_gasto', models.AutoField(primary_key=True, serialize=False)),
                ('monto_total', models.BigIntegerField()),
                ('fecha', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Gasto',
                'verbose_name_plural': 'Gastos',
            },
        ),
        migrations.CreateModel(
            name='DetalleGasto',
            fields=[
                ('id_detalle_gasto', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
                ('precio_unitario', models.BigIntegerField()),
                ('gasto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_cobros.gasto')),
            ],
            options={
                'verbose_name': 'Detalle de gasto',
                'verbose_name_plural': 'Detalles de gasto',
            },
        ),
        migrations.CreateModel(
            name='DetalleComprobante',
            fields=[
                ('id_detalle_comprobante', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.IntegerField()),
                ('comprobante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_cobros.comprobantegasto')),
            ],
            options={
                'verbose_name': 'Detalle de Comprobante',
                'verbose_name_plural': 'Detalles de comprobante',
            },
        ),
        migrations.AddField(
            model_name='comprobantegasto',
            name='gasto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_cobros.gasto'),
        ),
        migrations.AddField(
            model_name='detallecaja',
            name='gasto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_cobros.gasto'),
        ),
    ]
