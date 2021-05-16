from django.shortcuts import render, redirect
from .models import CLIENTE, PROVEEDOR, PRODUCTO, ORDEN_PEDIDO
from django.contrib import messages
from django import forms
from src.forms import FormCliente, FormProveedor, FormProducto, FormPedido, FormRegistroEdit

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


def Login(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    if request.method == 'POST':
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            messages.warning(request, 'Usuario o contraseña incorrectos')
        
    return render(request, 'registration/login.html')


@login_required(login_url="login")
def Index(request):
    return render(request, 'index.html')


##**************************Usuarios***************************************
@method_decorator(login_required, name='dispatch')
class UsuarioListado(ListView): 
    model = User 
    template_name = "usuarios/listar.html"

@login_required(login_url="login")
def UsuarioCrear(request):

    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    is_superuser = request.POST.get('is_superuser')

    if is_superuser == 'on':
        is_superuser = True
    else:
        is_superuser = False

    validarEmail = User.objects.filter(email = email)
    validarUsuario = User.objects.filter(username = username)
    
    if request.method == 'POST':
        if validarEmail:
            messages.warning(request, 'el email ya existe')
        elif validarUsuario:
            messages.warning(request, 'el usuario ya existe')
        else:
            if (ValidacionCamposUsuario(request,
                username, first_name, last_name, email, password1, password2)
            ):
                user = User.objects.create_user(
                    username = username, 
                    first_name = first_name, 
                    last_name = last_name, 
                    email = email, 
                    is_superuser = is_superuser,
                    is_active = True
                    )
                user.set_password(password1)
                user.set_password(password2)

                if user is not None:
                    user.save()
                    messages.warning(request, 'Usuario creado correctamente')
                    return redirect('listarUsuarios')
                else:
                    messages.warning(request, 'No se pudo crear usuario')
        
    return render(request, 'usuarios/crear.html')


import re
def ValidacionCamposUsuario(request, username, first_name, last_name, email, password1, password2):
    estado = False
    username.strip()
    first_name.strip()
    last_name.strip()
    email.strip()
    password1.strip()
    password2.strip()
    
    if len(username) < 4:
        messages.warning(request, 'La cantidad de caracteres del usuario debe ser mayor a 3')
    elif len(username) > 150:
        messages.warning(request, 'La cantidad de caracteres del usuario debe ser menor a 151')
    elif len(first_name) < 3:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser mayor a 2')
    elif len(first_name) > 150:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser menor a 151')
    elif len(last_name) < 3:
        messages.warning(request, 'La cantidad de caracteres del apellido debe ser mayor a 2')
    elif len(last_name) > 150:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser menor a 151')
    elif len(email) < 4:
        messages.warning(request, 'La cantidad de caracteres del email debe ser mayor a 3')
    elif len(email) > 254:
        messages.warning(request, 'La cantidad de caracteres del email debe ser menor a 255')
    elif len(password1) < 4:
        messages.warning(request, 'La cantidad de caracteres de la contraseña debe ser mayor a 3')
    elif len(password1) > 128:
        messages.warning(request, 'La cantidad de caracteres de la contraseña debe ser menor a 129')
    elif password2 != password1:
        messages.warning(request, 'Las contraseñas tienen que ser iguales')
    else:
        if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',email.lower()):
            estado = True
        else:
            messages.warning(request, 'El correo no cumple con la estructura basica')

    return estado


def UsuarioActualizar(request, id):

    user = User.objects.get(id=id)
    form = FormRegistroEdit(request.POST or None, instance=user)
    # email = request.POST.get('email')
    # validarEmail = User.objects.filter(email = email)
    
    if form.is_valid():
        
        form.save()
        messages.warning(request, 'Usuario editado correctamente')
        return redirect('listarUsuarios')
    
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    return render(request, 'usuarios/actualizar.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class UsuarioDetalle(DetailView): 
    model = User 

def DesactivarUsuario(request, id):
    user = User.objects.get(id = id)
    user.is_active = False
    user.save()
    messages.warning(request, f'Usuario {user.first_name} desactivado')
    return redirect('listarUsuarios')

def ActivarUsuario(request, id):
    user = User.objects.get(id = id)
    user.is_active = True
    user.save()
    messages.warning(request, f'Usuario {user.first_name} activado')
    return redirect('listarUsuarios')


##*************************************************************************

##**************************Clientes***************************************
@method_decorator(login_required, name='dispatch')
class ClienteListado(ListView):
    model = CLIENTE

@method_decorator(login_required, name='dispatch')
class ClienteCrear(SuccessMessageMixin, CreateView, ListView):
    model = CLIENTE
    form = FormCliente()
    fields = "__all__"
    success_message = 'Cliente creado correctamente'

    def get_success_url(self):
        return reverse('listarClientes')

@method_decorator(login_required, name='dispatch')
class ClienteDetalle(DetailView):
    model = CLIENTE

@method_decorator(login_required, name='dispatch')
class ClienteActualizar(SuccessMessageMixin, UpdateView):
    model = CLIENTE
    form = FormCliente()
    fields = "__all__"
    success_message = 'Cliente actualizado correctamente'
    def get_success_url(self):
        return reverse('listarClientes')

##******************************************************************

##**************************Proveedor***************************************
@method_decorator(login_required, name='dispatch')
class ProveedorListado(ListView):
    model = PROVEEDOR

@method_decorator(login_required, name='dispatch')
class ProveedorCrear(SuccessMessageMixin, CreateView, ListView):
    model = PROVEEDOR
    form = FormProveedor()
    fields = "__all__"
    success_message = 'Proveedor creado correctamente'

    def get_success_url(self):
        return reverse('listarProveedores')

@method_decorator(login_required, name='dispatch')
class ProveedorDetalle(DetailView):
    model = PROVEEDOR

@method_decorator(login_required, name='dispatch')
class ProveedorActualizar(SuccessMessageMixin, UpdateView):
    model = PROVEEDOR
    form = FormProveedor()
    fields = "__all__"
    success_message = 'Proveedor actualizado correctamente'
    def get_success_url(self):
        return reverse('listarProveedores')

##******************************************************************

##**************************Producto***************************************
@method_decorator(login_required, name='dispatch')
class ProductoListado(ListView):
    model = PRODUCTO

@method_decorator(login_required, name='dispatch')
class ProductoCrear(SuccessMessageMixin, CreateView, ListView):
    model = PRODUCTO
    form = FormProducto()
    fields = "__all__"
    success_message = 'Producto creado correctamente'

    def get_success_url(self):
        return reverse('listarProductos')

@method_decorator(login_required, name='dispatch')
class ProductoDetalle(DetailView):
    model = PRODUCTO

@method_decorator(login_required, name='dispatch')
class ProductoActualizar(SuccessMessageMixin, UpdateView):
    model = PRODUCTO
    form = FormProducto()
    fields = "__all__"
    success_message = 'Producto actualizado correctamente'
    def get_success_url(self):
        return reverse('listarProductos')

##********************************************************************


##**************************Pedidos********************
@method_decorator(login_required, name='dispatch')
class PedidosListado(ListView):
    model = ORDEN_PEDIDO

@method_decorator(login_required, name='dispatch')
class PedidosCrear(SuccessMessageMixin, CreateView, ListView):
    model = ORDEN_PEDIDO
    form = FormPedido()
    fields = "__all__"
    success_message = 'Pedido creado correctamente'

@method_decorator(login_required, name='dispatch')
class PedidosDetalle(DetailView):
    model = ORDEN_PEDIDO

@method_decorator(login_required, name='dispatch')
class PedidosActualizar(SuccessMessageMixin, UpdateView):
    model = ORDEN_PEDIDO
    form = FormPedido()
    fields = "__all__"
    success_message = 'Pedido actualizado correctamente'
    def get_success_url(self):
        return reverse('listarPedidos')

##******************************************************************
