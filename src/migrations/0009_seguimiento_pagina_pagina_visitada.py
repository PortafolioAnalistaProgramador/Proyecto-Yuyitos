# Generated by Django 3.2 on 2021-05-31 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0008_auto_20210531_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='seguimiento_pagina',
            name='pagina_visitada',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
