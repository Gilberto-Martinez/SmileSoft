# Generated by Django 3.1.13 on 2022-10-13 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_agendamiento', '0012_auto_20221011_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='tratamiento_simple',
            field=models.CharField(choices=[('CONSULTA DE DIAGNOSTICO', 'CONSULTA DE DIAGNOSTICO'), ('CHEQUEO DE RUTINA', 'CHEQUEO DE RUTINA'), ('CONTROL Y SEGUIMIENTO DEL TRATAMIENTO', 'CONTROL Y SEGUIMIENTO DEL TRATAMIENTO'), ('ORTODONCIA | CHEQUEO DE BRACKETS', 'ORTODONCIA | CHEQUEO DE BRACKETS ')], max_length=300, null=True, verbose_name='Motivo de la Consulta'),
        ),
    ]
