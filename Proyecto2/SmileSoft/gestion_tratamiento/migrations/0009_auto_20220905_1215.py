# Generated by Django 3.1.13 on 2022-09-05 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0008_tratamientoinsumo_cantidad'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tratamiento',
            options={'verbose_name': 'tratamiento', 'verbose_name_plural': 'tratamientos'},
        ),
        migrations.RemoveField(
            model_name='tratamiento',
            name='insumos',
        ),
        migrations.DeleteModel(
            name='TratamientoInsumo',
        ),
    ]
