# Generated by Django 3.1.13 on 2022-07-14 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inventario_insumos', '0010_auto_20220713_2032'),
        ('gestion_tratamiento', '0006_delete_horario'),
    ]

    operations = [
        migrations.CreateModel(
            name='TratamientoInsumo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insumo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_inventario_insumos.insumo')),
                ('tratamiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_tratamiento.tratamiento')),
            ],
            options={
                'db_table': 'TratamientoInsumo',
            },
        ),
        migrations.AddField(
            model_name='tratamiento',
            name='insumos',
            field=models.ManyToManyField(through='gestion_tratamiento.TratamientoInsumo', to='gestion_inventario_insumos.Insumo'),
        ),
    ]