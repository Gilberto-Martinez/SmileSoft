# Generated by Django 3.1.13 on 2022-08-20 01:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_agendamiento', '0009_horario'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='hora_atencion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_agendamiento.horario', verbose_name='Hora de atencion'),
        ),
    ]
