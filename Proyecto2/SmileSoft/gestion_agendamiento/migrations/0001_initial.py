# Generated by Django 3.1.13 on 2022-06-24 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion_tratamiento', '0004_auto_20220523_1511'),
        ('gestion_administrativo', '0043_auto_20220623_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id_cita', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_administrativo.paciente')),
                ('tratamiento_solicitado', models.OneToOneField(max_length=45, on_delete=django.db.models.deletion.PROTECT, to='gestion_tratamiento.tratamiento', verbose_name='Motivo de consulta')),
            ],
            options={
                'verbose_name_plural': 'Cita',
            },
        ),
    ]
