# Generated by Django 3.2 on 2021-05-23 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0004_alter_producto_codigo_barra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='codigo_barra',
            field=models.CharField(default=None, max_length=18),
        ),
    ]
