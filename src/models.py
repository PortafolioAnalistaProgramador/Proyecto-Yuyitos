from django.db import models

class CLIENTE(models.Model):
    run = models.CharField(max_length=10, default=None)
    nombre = models.CharField(max_length=100, default=None)
    telefono = models.CharField(max_length=12, default=None)
    correo = models.CharField(max_length=128, default=None)
    direccion = models.CharField(max_length=150, default=None)
    estado = models.IntegerField(default=None)

class PAGO_FIADO(models.Model):
    estado = models.IntegerField(default=None)
    monto = models.IntegerField(default=None)
    fecha = models.DateTimeField()
    fecha_final = models.DateTimeField()

class DETALLE_FIADO(models.Model):
    monto_abonado = models.IntegerField(default=None)
    pago_fiado = models.ForeignKey(PAGO_FIADO, on_delete=models.CASCADE, default=None)
    fecha_abono = models.DateTimeField(auto_now_add=False, auto_now=True)
    cliente = models.ForeignKey(CLIENTE, on_delete=models.CASCADE, default=None, blank=True)
    
class TIPO_USUARIO(models.Model):
    rol = models.CharField(max_length=50, default=None)

    def  __str__(self):
        return self.rol

class USUARIO(models.Model):
    usuario = models.CharField(max_length=128, default=None)
    contrasena = models.CharField(max_length=128, default=None)
    tipo_usuario = models.ForeignKey(TIPO_USUARIO, on_delete=models.CASCADE, default=None)

class VENTA(models.Model):
    fecha_venta = models.DateTimeField(auto_now_add=False, auto_now=True)
    total_a_pagar = models.IntegerField(default=None)
    usuario = models.ForeignKey(USUARIO, on_delete=models.CASCADE, default=None, blank=True)
    cliente = models.ForeignKey(CLIENTE, on_delete=models.CASCADE, default=None, blank=True)

class TIPO_PRODUCTO(models.Model):
    descripcion = models.CharField(max_length=150, default=None)

class FAMILIA_PRODUCTO(models.Model):
    tipo_producto = models.ForeignKey(TIPO_PRODUCTO, on_delete=models.CASCADE, default=None, blank=True)
    descripcion = models.CharField(max_length=100, default=None)

class PRODUCTO(models.Model):
    nombre = models.CharField(max_length=100, default=None)
    stock = models.IntegerField(default=None)
    precio = models.IntegerField(default=None)
    descripcion = models.CharField(max_length=200, default=None, blank=True)
    precio_compra = models.IntegerField(default=None)
    stock_critico = models.IntegerField(default=None)
    estado = models.IntegerField(default=None)
    fecha_vencimiento = models.DateTimeField(blank=True)
    codigo_barra = models.IntegerField(default=None)
    familia_producto = models.ForeignKey(FAMILIA_PRODUCTO, on_delete=models.CASCADE, default=None, blank=True)

class DETALLE_VENTA(models.Model):
    venta = models.ForeignKey(VENTA, on_delete=models.CASCADE, default=None)
    producto = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE, default=None, blank=True)
    cantidad = models.IntegerField(default=None)
    monto_a_pagar = models.IntegerField(default=None)

class CATEGORIA_PROVEEDOR(models.Model):
    descripcion = models.CharField(max_length=100, default=None)

class PROVEEDOR(models.Model):
    correo = models.CharField(max_length=100, default=None)
    telefono = models.CharField(max_length=12, default=None)
    razon_social = models.CharField(max_length=100, default=None)
    direccion = models.CharField(max_length=150, default=None)
    categoria_proveedor = models.ForeignKey(CATEGORIA_PROVEEDOR, on_delete=models.CASCADE, default=None, blank=True)
    estado = models.IntegerField(default=None)

class ORDEN_PEDIDO(models.Model):
    estado_recepcion = models.IntegerField(default=None)
    proveedor = models.ForeignKey(PROVEEDOR, on_delete=models.CASCADE, default=None)
    fecha_pedido = models.DateTimeField(auto_now_add=False, auto_now=True)
    fecha_recepcion = models.DateTimeField(blank=True)
    

class DETALLE_ORDEN(models.Model):
    cantidad = models.IntegerField(default=None)
    producto = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE, default=None, blank=True)
    orden_pedido = models.ForeignKey(ORDEN_PEDIDO, on_delete=models.CASCADE, default=None)



# class COMUNA(models.Model):
#     nombre = models.CharField(max_length=200, default=None)
#     localidad = models.ForeignKey(LOCALIDAD,on_delete=models.CASCADE,default=None)
    
#     def  __str__(self):
#         return self.nombre
    
# class CATEGORIA(models.Model):
#     nombre = models.CharField(max_length=200, default=None)
#     def  __str__(self):
#         return self.nombre
    
# class TIPO_PRODUCTO(models.Model):
#     nombre = models.CharField(max_length=200, default=None)
#     categoria = models.ForeignKey(CATEGORIA,on_delete=models.CASCADE,default=None)
#     def  __str__(self):
#         return self.nombre

# #importar datetime   
# #end_date = models.DateTimeField(auto_now_add=True)
