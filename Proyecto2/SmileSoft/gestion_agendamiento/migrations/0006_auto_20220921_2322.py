# Generated by Django 3.1.13 on 2022-09-22 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_administrativo', '0057_auto_20220823_2203'),
        ('gestion_agendamiento', '0005_cita_celular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='celular',
            field=models.ForeignKey(max_length=40, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_administrativo.persona'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gestion_administrativo.paciente'),
        ),
    ]