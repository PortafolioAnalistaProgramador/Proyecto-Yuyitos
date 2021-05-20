from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CLIENTE, PROVEEDOR, PRODUCTO, ORDEN_PEDIDO


        

# class FormRegistroEdit(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ("username","first_name","last_name","email","password1","password2","is_superuser")
        
class FormRegistroEdit(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password1","password2","is_superuser")

class FormCliente(forms.ModelForm):
    
    class Meta:
        model = CLIENTE
        fields = ("run","nombre","telefono","correo","direccion")

class FormProducto(forms.ModelForm):
    
    class Meta:
        model = PRODUCTO
        fields = ("nombre","precio","descripcion","precio_compra","stock","stock_critico","estado","fecha_vencimiento","codigo_barra","familia_producto")

class FormProveedor(forms.ModelForm):

    class Meta:
        model = PROVEEDOR
        fields = ("categoria_proveedor",)

class FormProveedorAct(forms.ModelForm):
    
    class Meta:
        model = PROVEEDOR
        fields = ("razon_social","correo","telefono","direccion","categoria_proveedor")

class FormPedido(forms.ModelForm):

    class Meta:
        model = ORDEN_PEDIDO
        fields = ("id","estado_recepcion","proveedor","fecha_llegada","fecha_recepcion","hora_recepcion") 


# class FormCliente(forms.Form):
#     run = forms.CharField(
#         label = "Run"
#     )

#     Nombre = forms.CharField(
#         label = "Nombre"
#     )

#     telefono = forms.IntegerField(
#         label = "Telefono"
#     )

#     correo = forms.CharField(
#         label = "Correo"
#     )
    
#     direccion = forms.CharField(
#         label = "Direccion"
#     )

#     options = [
#         (1,'Si'),
#         (0,'No')
#     ]
    
#     estado = forms.TypedChoiceField(
#         label = "Se le puede dar fiado?",
#         choices = options
#     )

    