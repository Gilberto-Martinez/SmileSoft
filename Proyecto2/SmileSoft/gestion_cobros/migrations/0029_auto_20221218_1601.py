# Generated by Django 3.1.13 on 2022-12-18 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cobros', '0028_auto_20221216_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprobantegasto',
            name='fecha',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='comprobantegasto',
            name='monto_total',
            field=models.BigIntegerField(null=True),
        ),
    ]
