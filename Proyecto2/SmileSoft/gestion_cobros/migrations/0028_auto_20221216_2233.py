# Generated by Django 3.1.13 on 2022-12-17 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cobros', '0027_delete_gasto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comprobantegasto',
            old_name='total_monto',
            new_name='monto_total',
        ),
        migrations.AddField(
            model_name='comprobantegasto',
            name='razon_social',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='comprobantegasto',
            name='timbrado',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='comprobantegasto',
            name='total_iva_10',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='comprobantegasto',
            name='total_iva_5',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='detallecomprobante',
            name='iva_10',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='detallecomprobante',
            name='iva_5',
            field=models.FloatField(null=True),
        ),
    ]
