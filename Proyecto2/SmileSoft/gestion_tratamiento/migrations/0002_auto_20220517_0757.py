# Generated by Django 3.1.13 on 2022-05-17 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tratamiento',
            name='codigo_tratamiento',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Código de tratamiento (*):'),
        ),
        migrations.AlterField(
            model_name='tratamiento',
            name='descripcion_tratamiento',
            field=models.TextField(max_length=500, null=True, verbose_name='Descripción (*):'),
        ),
        migrations.AlterField(
            model_name='tratamiento',
            name='nombre_tratamiento',
            field=models.CharField(max_length=40, verbose_name='nombre (*):'),
        ),
        migrations.AlterField(
            model_name='tratamiento',
            name='precio',
            field=models.IntegerField(verbose_name='precio (*):'),
        ),
    ]
