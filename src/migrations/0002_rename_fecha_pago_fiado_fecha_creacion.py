# Generated by Django 3.2 on 2021-06-21 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pago_fiado',
            old_name='fecha',
            new_name='fecha_creacion',
        ),
    ]