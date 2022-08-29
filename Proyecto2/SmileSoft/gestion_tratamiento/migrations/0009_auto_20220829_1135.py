# Generated by Django 3.1.13 on 2022-08-29 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inventario_insumos', '0014_auto_20220818_1450'),
        ('gestion_tratamiento', '0008_tratamientoinsumo_cantidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='TratamientoInsumoAsignado',
            fields=[
                ('id_insumo_asig', models.AutoField(primary_key=True, serialize=False)),
                ('insumo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_inventario_insumos.insumo')),
            ],
            options={
                'db_table': 'TratamientoInsumoAsignado',
            },
        ),
        migrations.AlterModelOptions(
            name='tratamiento',
            options={'ordering': ['codigo_tratamiento'], 'verbose_name': 'tratamiento', 'verbose_name_plural': 'tratamientos'},
        ),
        migrations.DeleteModel(
            name='TratamientoInsumo',
        ),
        migrations.AddField(
            model_name='tratamientoinsumoasignado',
            name='tratamiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_tratamiento.tratamiento'),
        ),
        migrations.AlterField(
            model_name='tratamiento',
            name='insumos',
            field=models.ManyToManyField(related_name='tratamiento_set', through='gestion_tratamiento.TratamientoInsumoAsignado', to='gestion_inventario_insumos.Insumo'),
        ),
    ]
