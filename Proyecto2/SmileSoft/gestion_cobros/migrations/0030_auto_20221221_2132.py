# Generated by Django 3.1.13 on 2022-12-22 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cobros', '0029_auto_20221218_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='cobrocontado',
            name='monto_efectivo',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='cobrocontado',
            name='vuelto',
            field=models.IntegerField(null=True),
        ),
    ]
