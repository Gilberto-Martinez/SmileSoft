# Generated by Django 3.1.13 on 2022-10-10 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_administrativo', '0061_auto_20221010_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pacientetratamientoasignado',
            name='estado',
        ),
    ]
