from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BOLETA, CLIENTE, FAMILIA_PRODUCTO, PROVEEDOR, PRODUCTO, ORDEN_PEDIDO, TIPO_PRODUCTO
# from django.utils import timezone

        

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

class FormProductoEdit(forms.ModelForm):
    
    class Meta:
        model = PRODUCTO
        fields = ("nombre","precio","descripcion","precio_compra","stock","stock_critico","codigo_barra","familia_producto")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
                'class': 'form-control'  
            })  
        self.fields['codigo_barra'].widget.attrs['readonly'] = True 
        self.fields['precio'].widget.attrs['readonly'] = True


class FormProducto(forms.ModelForm):
    
    class Meta:
        model = PRODUCTO
        fields = ("familia_producto",)

class FormFamiliaProd(forms.ModelForm):
    
    class Meta:
        model = FAMILIA_PRODUCTO
        fields = ("tipo_producto",)

class FormProductoProv(forms.ModelForm):
    
    class Meta:
        model = ORDEN_PEDIDO
        fields = ("proveedor",)

class FormClientesParaVenta(forms.ModelForm):
    
    class Meta:
        model = BOLETA
        fields = ("cliente",)

# class FormFechaProd(forms.ModelForm):

#     fecha_vencimiento = forms.TimeField(input_formats=['%I:%M %p'])
    
#     class Meta:
#         model = PRODUCTO
#         fields = ("fecha_vencimiento",)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs) 
#         for field in iter(self.fields):  
#             self.fields[field].widget.attrs.update({  
#                 'class': 'form-control'  
#             })  
#         # self.fields['fecha_vencimiento'].widget.attrs['readonly'] = True  

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

    