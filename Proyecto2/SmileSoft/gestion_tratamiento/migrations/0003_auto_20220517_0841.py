# Generated by Django 3.1.13 on 2022-05-17 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0002_auto_20220517_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tratamiento',
            name='nombre_tratamiento',
            field=models.CharField(max_length=100, verbose_name='nombre (*):'),
        ),
    ]
