# Generated by Django 3.1.13 on 2022-04-22 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_administrativo', '0007_auto_20220422_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente',
            name='afecciones_graves',
        ),
        migrations.AlterField(
            model_name='paciente',
            name='afeccion_cronica_familiar',
            field=models.TextField(max_length=500, null=True, verbose_name='Afección crónica familiar (*)'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='alergia',
            field=models.TextField(max_length=200, null=True, verbose_name='Alergia (*)'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='enfermedad_base',
            field=models.TextField(max_length=200, null=True, verbose_name='Enfermedad de base (*)'),
        ),
    ]
