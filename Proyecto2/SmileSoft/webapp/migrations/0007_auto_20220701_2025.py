# Generated by Django 3.1.13 on 2022-07-02 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0017_auto_20220326_1942'),
        ('webapp', '0006_auto_20220629_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
    ]
