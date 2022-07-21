# Generated by Django 3.1.13 on 2022-07-21 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_administrativo', '0045_auto_20220713_2140'),
        ('gestion_agendamiento', '0007_auto_20220712_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='profesional',
            field=models.ForeignKey(default=1, max_length=45, on_delete=django.db.models.deletion.PROTECT, to='gestion_administrativo.especialidad', verbose_name='Profesional a elegir'),
            preserve_default=False,
        ),
    ]
