# Generated by Django 3.1.13 on 2022-08-11 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0008_tratamientoinsumo_cantidad'),
        ('gestion_administrativo', '0052_remove_paciente_id_historial_clinico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pacientetratamientoasignado',
            name='estado',
        ),
        migrations.CreateModel(
            name='TratamientoConfirmado',
            fields=[
                ('id_tratamiento_conf', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Realizado', 'Realizado'), ('Confirmado', 'Confirmado')], default='Pendiente', max_length=12)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_administrativo.paciente')),
                ('tratamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_tratamiento.tratamiento')),
            ],
            options={
                'db_table': 'TratamientoConfirmado',
            },
        ),
    ]
