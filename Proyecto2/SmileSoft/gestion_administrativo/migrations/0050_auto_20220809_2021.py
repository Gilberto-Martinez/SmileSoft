# Generated by Django 3.1.13 on 2022-08-10 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_historial_clinico', '0002_auto_20220806_1241'),
        ('gestion_administrativo', '0049_pacientetratamientoasignado_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='id_historial_clinico',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_historial_clinico.historialclinico'),
        ),
        migrations.AddField(
            model_name='pacientetratamientoasignado',
            name='id_tratamiento_asig',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pacientetratamientoasignado',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Realizado', 'Realizado'), ('Confirmado', 'Confirmado')], default='Pendiente', max_length=12),
        ),
    ]