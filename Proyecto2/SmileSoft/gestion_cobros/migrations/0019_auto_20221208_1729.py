# Generated by Django 3.1.13 on 2022-12-08 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0016_auto_20221028_1551'),
        ('gestion_cobros', '0018_delete_detallecobrocontado'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DetalleCobroTratamiento',
            new_name='DetalleCobro',
        ),
    ]
