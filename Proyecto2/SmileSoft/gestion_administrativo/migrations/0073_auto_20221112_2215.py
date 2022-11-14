# Generated by Django 3.1.13 on 2022-11-13 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_administrativo', '0072_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='correo_electronico',
            field=models.EmailField(max_length=35, verbose_name='Correo electrónico:'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='direccion',
            field=models.CharField(max_length=200, null=True, verbose_name='Dirección:'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='f_fin_vigencia',
            field=models.DateField(verbose_name='Fecha Fin Vigencia:'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='f_inicio_vigencia',
            field=models.DateField(verbose_name='Fecha Inicio Vigencia:'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='nombre_empresa',
            field=models.CharField(max_length=40, verbose_name='Empresa:'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='telefono',
            field=models.CharField(max_length=20, null=True, verbose_name='Teléfono:'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='timbrado',
            field=models.IntegerField(verbose_name='Timbrado:'),
        ),
    ]
