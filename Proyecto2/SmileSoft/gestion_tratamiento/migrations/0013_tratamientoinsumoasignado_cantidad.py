# Generated by Django 3.1.13 on 2022-09-29 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0012_auto_20220928_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='tratamientoinsumoasignado',
            name='cantidad',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]