# Generated by Django 3.1.13 on 2022-12-08 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cobros', '0015_detallecobrotratamiento_cobro_contado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallecobrocontado',
            name='tratamientos',
        ),
    ]
