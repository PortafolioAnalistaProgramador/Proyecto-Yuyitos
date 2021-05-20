from django.shortcuts import render, redirect
from .models import CATEGORIA_PROVEEDOR, CLIENTE, PROVEEDOR, PRODUCTO, ORDEN_PEDIDO
from django.contrib import messages
from django import forms
from src.forms import FormCliente, FormProveedor, FormProducto, FormPedido, FormRegistroEdit, FormProveedorAct

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
                username.strip()
                first_name.strip()
                last_name.strip()
                email.strip()
                password1.strip()
                password2.strip()

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

@login_required(login_url="login")
def UsuarioActualizar(request, id):

    user = User.objects.get(id=id)
    form = FormRegistroEdit(request.POST or None, instance=user)

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

    if request.method == 'POST':
        if (ValidacionCamposUsuario(request,
            username, first_name, last_name, email, password1, password2)
        ):
            if user is not None:

                user.username = username.strip()
                user.save()
                user.first_name = first_name.strip()
                user.save()
                user.last_name = last_name.strip()
                user.save()
                user.email = email.strip()
                user.save()
                user.password1 = password1.strip()
                user.save()
                user.password2 = password2.strip()
                user.save()
                user.is_superuser = is_superuser
                user.save()
                messages.warning(request, 'Usuario actualizado correctamente')
                return redirect('listarUsuarios')
            else:
                messages.warning(request, 'No se pudo actualizar el usuario')
        else:
            messages.warning(request, 'No se pudo actualizar el usuario')
    
    return render(request, 'usuarios/actualizar.html', {'form':form})

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

@login_required(login_url="login")
def ClienteCrear(request):

    run = request.POST.get('run')
    nombre = request.POST.get('nombre')
    telefono = request.POST.get('telefono')
    correo = request.POST.get('correo')
    direccion = request.POST.get('direccion')
    validarRun = CLIENTE.objects.filter(run=run)

    if request.method == 'POST':
        if validarRun:
            messages.warning(request, 'el run ya existe')
        else:
            if (ValidacionCamposCliente(request,
                run, nombre, telefono, correo, direccion)
            ):
                cliente = CLIENTE.objects.create(
                    run = run.strip(),
                    nombre = nombre.strip(),
                    telefono = telefono.strip(),
                    correo = correo.strip(),
                    direccion = direccion.strip(),
                    estado = 1
                )

                if cliente is not None:
                    cliente.save()
                    messages.warning(request, 'Cliente creado correctamente')
                    return redirect('listarClientes')
                else:
                    messages.warning(request, 'No se pudo crear el cliente')
            else:
                messages.warning(request, 'No se pudo crear el cliente')
    
    return render(request, 'clientes/crear.html')

@login_required(login_url="login")
def ClienteActualizar(request, id):

    cliente = CLIENTE.objects.get(id=id)
    form = FormCliente(request.POST or None, instance=cliente)

    run = request.POST.get('run')
    nombre = request.POST.get('nombre')
    telefono = request.POST.get('telefono')
    correo = request.POST.get('correo')
    direccion = request.POST.get('direccion')
    validarRun = CLIENTE.objects.filter(run=run)

    if request.method == 'POST':
        if (ValidacionCamposCliente(request,
            run, nombre, telefono, correo, direccion)
        ):
            if cliente is not None:

                cliente.run = run.strip()
                cliente.save()
                cliente.nombre = nombre.strip()
                cliente.save()
                cliente.telefono = telefono.strip()
                cliente.save()
                cliente.correo = correo.strip()
                cliente.save()
                cliente.direccion = direccion.strip()
                cliente.save()
                messages.warning(request, 'Cliente actualizado correctamente')
                return redirect('listarClientes')
            else:
                messages.warning(request, 'No se pudo actualizar el cliente')
        else:
            messages.warning(request, 'No se pudo actualizar el cliente')
    
    return render(request, 'clientes/actualizar.html', {'form':form})

def ValidacionCamposCliente(request, run, nombre, telefono, correo, direccion):

    estado = False
    run.strip()
    nombre.strip()
    telefono.strip()
    correo.strip()
    direccion.strip()

    if len(run) < 7:
        messages.warning(request, 'La cantidad de caracteres del run debe ser mayor a 6')
    elif len(run) > 10:
        messages.warning(request, 'La cantidad de caracteres del run debe ser menor a 11')
    elif len(nombre) < 3:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser mayor a 2')
    elif len(nombre) > 100:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser menor a 101')
    elif len(telefono) < 5:
        messages.warning(request, 'La cantidad de caracteres del telefono debe ser mayor a 4')
    elif len(telefono) > 12:
        messages.warning(request, 'La cantidad de caracteres del telefono debe ser menor a 13')
    elif len(correo) < 5:
        messages.warning(request, 'La cantidad de caracteres del correo debe ser mayor a 4')
    elif len(correo) > 128:
        messages.warning(request, 'La cantidad de caracteres del correo debe ser menor a 129')
    elif len(direccion) < 3:
        messages.warning(request, 'La cantidad de caracteres de la direccion debe ser mayor a 2')
    elif len(direccion) > 150:
        messages.warning(request, 'La cantidad de caracteres de la direccion debe ser menor a 151')
    else:
        if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',correo.lower()):
            estado = True
        else:
            messages.warning(request, 'El correo no cumple con la estructura basica')

    return estado

@method_decorator(login_required, name='dispatch')
class ClienteDetalle(DetailView):
    model = CLIENTE

def DesactivarCliente(request, id):
    cliente = CLIENTE.objects.get(id = id)
    cliente.estado = 0
    cliente.save()
    messages.warning(request, f'Cliente {cliente.nombre} desactivado')
    return redirect('listarClientes')

def ActivarCliente(request, id):
    cliente = CLIENTE.objects.get(id = id)
    cliente.estado = 1
    cliente.save()
    messages.warning(request, f'Cliente {cliente.nombre} activado')
    return redirect('listarClientes')

##******************************************************************

##**************************Proveedor***************************************
@method_decorator(login_required, name='dispatch')
class ProveedorListado(ListView):
    model = PROVEEDOR


@login_required(login_url="login")
def ProveedorCrear(request):

    form = FormProveedor(request.POST)
    razon_social = request.POST.get('razon_social')
    correo = request.POST.get('correo')
    telefono = request.POST.get('telefono')
    direccion = request.POST.get('direccion')
    categoria = request.POST.get('categoria_proveedor')
    categoria = CATEGORIA_PROVEEDOR.objects.filter(id = categoria)
    for cat in categoria:
        categoria = cat
    
    if request.method == 'POST':
        
        if (ValidacionCamposProveedor(request,
            razon_social, correo, telefono, direccion)
        ):
            proveedor = PROVEEDOR.objects.create(
                razon_social = razon_social.strip(),
                correo = correo.strip(),
                telefono = telefono.strip(),
                direccion = direccion.strip(),
                categoria_proveedor = categoria,
                estado = 1
            )

            if proveedor is not None:
                proveedor.save()
                messages.warning(request, 'Proveedor creado correctamente')
                return redirect('listarProveedores')
            else:
                messages.warning(request, 'No se pudo crear el Proveedor')

    return render(request, 'proveedores/crear.html',{'form':form})

@login_required(login_url="login")
def ProveedorActualizar(request, id):

    proveedor = PROVEEDOR.objects.get(id=id)
    form = FormProveedorAct(request.POST or None, instance=proveedor)
    razon_social = request.POST.get('razon_social')
    correo = request.POST.get('correo')
    telefono = request.POST.get('telefono')
    direccion = request.POST.get('direccion')

    categoria = request.POST.get('categoria_proveedor')
    categoria = CATEGORIA_PROVEEDOR.objects.filter(id = categoria)
    for cat in categoria:
        categoria = cat

    if request.method == 'POST':
        if (ValidacionCamposProveedor(request,
            razon_social, correo, telefono, direccion)
        ):
            if proveedor is not None:

                proveedor.razon_social = razon_social.strip()
                proveedor.save()
                proveedor.correo = correo.strip()
                proveedor.save()
                proveedor.telefono = telefono.strip()
                proveedor.save()
                proveedor.direccion = direccion.strip()
                proveedor.save()
                proveedor.categoria_proveedor = categoria
                proveedor.save()

                messages.warning(request, 'Proveedor actualizado correctamente')
                return redirect('listarProveedores')
            else:
                messages.warning(request, 'No se pudo actualizar el proveedor')
        else:
            messages.warning(request, 'No se pudo actualizar el proveedor')
    
    return render(request, 'proveedores/actualizar.html', {'form':form})

def ValidacionCamposProveedor(request, razon_social, correo, telefono, direccion):
    estado = False
    razon_social.strip()
    correo.strip()
    telefono.strip()
    direccion.strip()

    if len(razon_social) < 3:
        messages.warning(request, 'La cantidad de caracteres de la razon social debe ser mayor a 2')
    elif len(razon_social) > 100:
        messages.warning(request, 'La cantidad de caracteres de la razon social debe ser menor a 11')
    elif len(correo) < 3:
        messages.warning(request, 'La cantidad de caracteres del correo debe ser mayor a 2')
    elif len(correo) > 100:
        messages.warning(request, 'La cantidad de caracteres del correo debe ser menor a 101')
    elif len(telefono) < 5:
        messages.warning(request, 'La cantidad de caracteres del telefono debe ser mayor a 4')
    elif len(telefono) > 12:
        messages.warning(request, 'La cantidad de caracteres del telefono debe ser menor a 13')
    elif len(direccion) < 3:
        messages.warning(request, 'La cantidad de caracteres de la direccion debe ser mayor a 2')
    elif len(direccion) > 150:
        messages.warning(request, 'La cantidad de caracteres de la direccion debe ser menor a 151')
    else:
        if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',correo.lower()):
            estado = True
        else:
            messages.warning(request, 'El correo no cumple con la estructura basica')

    return estado

@method_decorator(login_required, name='dispatch')
class ProveedorDetalle(DetailView):
    model = PROVEEDOR

def DesactivarProveedor(request, id):
    proveedor = PROVEEDOR.objects.get(id = id)
    proveedor.estado = 0
    proveedor.save()
    messages.warning(request, f'Proveedor {proveedor.razon_social} desactivado')
    return redirect('listarProveedores')

def ActivarProveedor(request, id):
    proveedor = PROVEEDOR.objects.get(id = id)
    proveedor.estado = 1
    proveedor.save()
    messages.warning(request, f'Cliente {proveedor.razon_social} activado')
    return redirect('listarProveedores')
    
##******************************************************************

##**************************Producto***************************************
@method_decorator(login_required, name='dispatch')
class ProductoListado(ListView):
    model = PRODUCTO

@method_decorator(login_required, name='dispatch')
class ProductoCrear(SuccessMessageMixin, CreateView):
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
class PedidosCrear(SuccessMessageMixin, CreateView):
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
