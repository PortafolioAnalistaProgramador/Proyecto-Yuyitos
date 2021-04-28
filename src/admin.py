from django.contrib import admin

from .models import CLIENTE, PAGO_FIADO, DETALLE_FIADO, BOLETA, TIPO_PRODUCTO, FAMILIA_PRODUCTO, PRODUCTO, DETALLE_BOLETA, CATEGORIA_PROVEEDOR, PROVEEDOR, ORDEN_PEDIDO, DETALLE_ORDEN


admin.site.register(CLIENTE)
admin.site.register(PAGO_FIADO)
admin.site.register(DETALLE_FIADO)
# admin.site.register(TIPO_USUARIO)
# admin.site.register(User)
admin.site.register(BOLETA)
admin.site.register(TIPO_PRODUCTO)
admin.site.register(FAMILIA_PRODUCTO)
admin.site.register(PRODUCTO)
admin.site.register(DETALLE_BOLETA)
admin.site.register(CATEGORIA_PROVEEDOR)
admin.site.register(PROVEEDOR)
admin.site.register(ORDEN_PEDIDO)
admin.site.register(DETALLE_ORDEN)