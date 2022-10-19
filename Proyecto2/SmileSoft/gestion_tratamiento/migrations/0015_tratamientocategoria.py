# Generated by Django 3.1.13 on 2022-10-19 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0014_auto_20220930_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='TratamientoCategoria',
            fields=[
                ('id_categoria_tratamiento', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_categoria', models.CharField(choices=[('Simple', 'Simple'), ('Complejo', 'Complejo')], default='Complejo', max_length=20, null=True)),
                ('categoria_tratamiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_tratamiento.tratamiento')),
            ],
        ),
    ]
