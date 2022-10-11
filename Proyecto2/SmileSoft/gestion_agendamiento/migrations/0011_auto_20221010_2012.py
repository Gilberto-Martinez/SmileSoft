# Generated by Django 3.1.13 on 2022-10-10 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0014_auto_20220930_1636'),
        ('gestion_agendamiento', '0010_auto_20221010_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='tratamiento_solicitado',
            field=models.ForeignKey(max_length=45, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_tratamiento.tratamiento', verbose_name='Tratamientos'),
        ),
    ]
