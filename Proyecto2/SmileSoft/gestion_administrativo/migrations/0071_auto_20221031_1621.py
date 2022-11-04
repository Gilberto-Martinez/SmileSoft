# Generated by Django 3.1.13 on 2022-10-31 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0016_auto_20221028_1551'),
        ('gestion_administrativo', '0070_delete_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='tratamientoconfirmado',
            name='especialista',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_administrativo.especialistasalud'),
        ),
        migrations.AlterField(
            model_name='tratamientoconfirmado',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_administrativo.paciente'),
        ),
        migrations.AlterField(
            model_name='tratamientoconfirmado',
            name='tratamiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_tratamiento.tratamiento'),
        ),
    ]
