# Generated by Django 3.1.13 on 2022-12-17 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cobros', '0022_auto_20221215_1808'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detallecaja',
            old_name='gasto',
            new_name='comprobante_pago',
        ),
        migrations.RemoveField(
            model_name='detallecaja',
            name='detalle',
        ),
    ]
