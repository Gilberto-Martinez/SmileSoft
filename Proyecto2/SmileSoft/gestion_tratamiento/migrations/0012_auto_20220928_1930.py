# Generated by Django 3.1.13 on 2022-09-28 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0011_tratamiento_insumos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tratamiento',
            options={'ordering': ['nombre_tratamiento'], 'verbose_name': 'tratamiento', 'verbose_name_plural': 'tratamientos'},
        ),
        migrations.AddField(
            model_name='tratamientoinsumoasignado',
            name='cantidad',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
