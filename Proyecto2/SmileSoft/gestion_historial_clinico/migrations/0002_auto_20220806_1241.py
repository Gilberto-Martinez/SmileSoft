# Generated by Django 3.1.13 on 2022-08-06 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0008_tratamientoinsumo_cantidad'),
        ('gestion_historial_clinico', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialclinico',
            name='numero_ficha',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='TratamientoRealizado',
            fields=[
                ('id_tratamiento_realizado', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_realizacion', models.DateField(auto_now_add=True)),
                ('codigo_tratamiento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_tratamiento.tratamiento', verbose_name='Código de tratamiento')),
                ('id_historial_clinico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_historial_clinico.historialclinico', verbose_name='Id de historial clinico')),
            ],
            options={
                'verbose_name': 'Tratamientos Realizados',
                'db_table': 'TratamientoRealizado',
            },
        ),
    ]
