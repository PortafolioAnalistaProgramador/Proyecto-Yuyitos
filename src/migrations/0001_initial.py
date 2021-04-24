# Generated by Django 3.1.7 on 2021-04-04 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CATEGORIA_PROVEEDOR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CLIENTE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run', models.CharField(default=None, max_length=10)),
                ('nombre', models.CharField(default=None, max_length=100)),
                ('telefono', models.CharField(default=None, max_length=12)),
                ('correo', models.CharField(default=None, max_length=128)),
                ('direccion', models.CharField(default=None, max_length=150)),
                ('estado', models.IntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='FAMILIA_PRODUCTO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PAGO_FIADO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.IntegerField(default=None)),
                ('monto', models.IntegerField(default=None)),
                ('fecha', models.DateTimeField()),
                ('fecha_final', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TIPO_PRODUCTO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(default=None, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='TIPO_USUARIO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(default=None, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='USUARIO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(default=None, max_length=128)),
                ('contrasena', models.CharField(default=None, max_length=128)),
                ('tipo_usuario', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='src.tipo_usuario')),
            ],
        ),
        migrations.CreateModel(
            name='VENTA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_venta', models.DateTimeField(auto_now=True)),
                ('total_a_pagar', models.IntegerField(default=None)),
                ('cliente', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='src.cliente')),
                ('usuario', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='src.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='PROVEEDOR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.CharField(default=None, max_length=100)),
                ('telefono', models.CharField(default=None, max_length=12)),
                ('razon_social', models.CharField(default=None, max_length=100)),
                ('direccion', models.CharField(default=None, max_length=150)),
                ('estado', models.IntegerField(default=None)),
                ('categoria_proveedor', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='src.categoria_proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='PRODUCTO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default=None, max_length=100)),
                ('stock', models.IntegerField(default=None)),
                ('precio', models.IntegerField(default=None)),
                ('descripcion', models.CharField(blank=True, default=None, max_length=200)),
                ('precio_compra', models.IntegerField(default=None)),
                ('stock_critico', models.IntegerField(default=None)),
                ('estado', models.IntegerField(default=None)),
                ('fecha_vencimiento', models.DateTimeField(blank=True)),
                ('codigo_barra', models.IntegerField(default=None)),
                ('familia_producto', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='src.familia_producto')),
            ],
        ),
        migrations.CreateModel(
            name='ORDEN_PEDIDO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_recepcion', models.IntegerField(default=None)),
                ('fecha_pedido', models.DateTimeField(auto_now=True)),
                ('fecha_recepcion', models.DateTimeField(blank=True)),
                ('proveedor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='src.proveedor')),
            ],
        ),
        migrations.AddField(
            model_name='familia_producto',
            name='tipo_producto',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='src.tipo_producto'),
        ),
        migrations.CreateModel(
            name='DETALLE_VENTA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=None)),
                ('monto_a_pagar', models.IntegerField(default=None)),
                ('producto', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='src.producto')),
                ('venta', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='src.venta')),
            ],
        ),
        migrations.CreateModel(
            name='DETALLE_ORDEN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=None)),
                ('orden_pedido', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='src.orden_pedido')),
                ('producto', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='src.producto')),
            ],
        ),
        migrations.CreateModel(
            name='DETALLE_FIADO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_abonado', models.IntegerField(default=None)),
                ('fecha_abono', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='src.cliente')),
                ('pago_fiado', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='src.pago_fiado')),
            ],
        ),
    ]