from django.db import models
from django.contrib.auth.models import User


estado_cliente = [
    (1,'Si'),
    (0,'No')
]

estado_proveedor = [
    (1,'Activo'),
    (0,'No activo')
]

estado_boleta = [
    (1,'Activa'),
    (0,'Anular')
]

estado_producto = [
    (1,'Disponible'),
    (0,'No disponible')
]



class CLIENTE(models.Model):
    run = models.CharField(max_length=10, default=None)
    nombre = models.CharField(max_length=100, default=None)
    telefono = models.CharField(max_length=12, default=None)
    correo = models.CharField(max_length=128, default=None)
    direccion = models.CharField(max_length=150, default=None)
    estado = models.IntegerField(default=None,choices=estado_cliente)

    def __str__(self):
        return self.nombre

class PAGO_FIADO(models.Model):
    estado = models.IntegerField(default=None)
    monto = models.IntegerField(default=None)
    fecha = models.DateTimeField(auto_now_add=False, auto_now=True)#agregar que el llenado de fecha se automatico en esta
    fecha_final = models.DateTimeField()

class DETALLE_FIADO(models.Model):
    monto_abonado = models.IntegerField(default=None)
    pago_fiado = models.ForeignKey(PAGO_FIADO, on_delete=models.CASCADE, default=None)
    fecha_abono = models.DateTimeField(auto_now_add=False, auto_now=True)
    cliente = models.ForeignKey(CLIENTE, on_delete=models.CASCADE, default=None, blank=True)
    
# class TIPO_USUARIO(models.Model):
#     rol = models.CharField(max_length=50, default=None)

#     def __str__(self):
#         return self.rol

class BOLETA(models.Model):
    fecha_boleta = models.DateTimeField(auto_now_add=False, auto_now=True)
    total_a_pagar = models.IntegerField(default=None)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True)
    cliente = models.ForeignKey(CLIENTE, on_delete=models.CASCADE, default=None, blank=True, null=True)
    estado = estado = models.IntegerField(default=None,choices=estado_boleta)
    
    class Meta:
        ordering = ['id']

class CATEGORIA_PROVEEDOR(models.Model):
    descripcion = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.descripcion

class PROVEEDOR(models.Model):
    razon_social = models.CharField(max_length=100, default=None)
    correo = models.CharField(max_length=100, default=None)
    telefono = models.CharField(max_length=12, default=None)
    direccion = models.CharField(max_length=150, default=None)
    categoria_proveedor = models.ForeignKey(CATEGORIA_PROVEEDOR, on_delete=models.CASCADE, default=None)
    estado = models.IntegerField(default=None, choices=estado_proveedor)

    def __str__(self):
        return self.razon_social

class TIPO_PRODUCTO(models.Model):
    descripcion = models.CharField(max_length=150, default=None)
    proveedor = models.ForeignKey(PROVEEDOR, on_delete=models.CASCADE, default=None, blank=True, null=True)
    
    def __str__(self):
        return self.descripcion

class FAMILIA_PRODUCTO(models.Model):
    tipo_producto = models.ForeignKey(TIPO_PRODUCTO, on_delete=models.CASCADE, default=None, blank=True)
    descripcion = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.descripcion

class PRODUCTO(models.Model):
    nombre = models.CharField(max_length=100, default=None)
    precio = models.IntegerField(default=None)
    descripcion = models.CharField(max_length=200, default=None, blank=True)
    precio_compra = models.IntegerField(default=None)
    stock = models.IntegerField(default=None)
    stock_critico = models.IntegerField(default=None)
    estado = models.IntegerField(default=None, choices=estado_producto)
    fecha_vencimiento = models.DateTimeField(blank=True)
    codigo_barra = models.CharField(max_length=18,default=None)
    familia_producto = models.ForeignKey(FAMILIA_PRODUCTO, on_delete=models.CASCADE, default=None, blank=True)

    def __str__(self):
        return self.nombre

class DETALLE_BOLETA(models.Model):
    boleta = models.ForeignKey(BOLETA, on_delete=models.CASCADE, default=None)
    cantidad = models.IntegerField(default=None)
    monto_a_pagar = models.IntegerField(default=None)
    producto = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE, default=None, blank=True)

class ORDEN_PEDIDO(models.Model):
    estado_recepcion = models.IntegerField(default=None)
    proveedor = models.ForeignKey(PROVEEDOR, on_delete=models.CASCADE, default=None)
    fecha_pedido = models.DateField(auto_now_add=False, auto_now=True)
    fecha_llegada = models.DateField(blank=True, null=True)
    fecha_recepcion = models.DateField(blank=True, null=True)
    hora_recepcion = models.TimeField(blank=True, null=True)

class DETALLE_ORDEN(models.Model):
    cantidad = models.IntegerField(default=None)
    orden_pedido = models.ForeignKey(ORDEN_PEDIDO, on_delete=models.CASCADE, default=None)
    producto = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE, default=None, blank=True)

class SEGUIMIENTO_PAGINA(models.Model):
    fecha_ingreso = models.DateTimeField(auto_now_add=False, auto_now=True)
    pagina_visitada = models.CharField(max_length=50, default=None)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True)


