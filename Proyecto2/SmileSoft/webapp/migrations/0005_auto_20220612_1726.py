# Generated by Django 3.1.13 on 2022-06-12 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0017_auto_20220326_1942'),
        ('webapp', '0004_auto_20220523_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
    ]