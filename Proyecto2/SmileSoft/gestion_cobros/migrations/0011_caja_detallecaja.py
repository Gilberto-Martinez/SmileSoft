# Generated by Django 3.1.13 on 2022-11-28 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_administrativo', '0073_auto_20221112_2215'),
        ('gestion_cobros', '0010_auto_20221122_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id_caja', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_apertura', models.DateField()),
                ('hora_apertura', models.TimeField()),
                ('fecha_cierre', models.DateField()),
                ('hora_cierre', models.TimeField()),
                ('monto_apertura', models.BigIntegerField()),
                ('monto_cierre', models.BigIntegerField()),
                ('id_cajero', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_administrativo.funcionario')),
            ],
            options={
                'verbose_name': 'Caja',
            },
        ),
        migrations.CreateModel(
            name='DetalleCaja',
            fields=[
                ('id_detalle_caja', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('Ingreso', 'Ingreso'), ('Egreso', 'Egreso')], default='Ingreso', max_length=7)),
                ('detalle', models.CharField(max_length=100)),
                ('id_caja', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_cobros.caja')),
                ('id_comprobante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_cobros.factura')),
            ],
            options={
                'verbose_name': 'Detalle de caja',
                'verbose_name_plural': 'Detalles de caja',
            },
        ),
    ]
