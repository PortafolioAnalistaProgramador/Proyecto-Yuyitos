from django.shortcuts import render, redirect
from .models import CATEGORIA_PROVEEDOR, CLIENTE, FAMILIA_PRODUCTO, PROVEEDOR, PRODUCTO, ORDEN_PEDIDO, SEGUIMIENTO_PAGINA, TIPO_PRODUCTO, BOLETA, DETALLE_BOLETA, PAGO_FIADO, DETALLE_FIADO, DETALLE_ORDEN
from django.contrib import messages
from django import forms
from src.forms import FormCliente, FormProveedor, FormProducto, FormPedido, FormRegistroEdit, FormProveedorAct, FormFamiliaProd, FormProductoProv, FormProductoEdit, FormClientesParaVenta, FormBoleta, FormClientesInforme, FormInformeOrdenPedido, FormSeguimientoPagina, FormCategProv
import openpyxl
from tempfile import NamedTemporaryFile
from datetime import datetime

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

@login_required(login_url="login")
def Venta(request):

    usuarioBoleta = request.user
    usuarioBoleta = User.objects.get(username=usuarioBoleta)

    seguimientoPag = SEGUIMIENTO_PAGINA.objects.create(
        pagina_visitada = "ventas",
        usuario = usuarioBoleta
    )
    seguimientoPag.save()

    productos = PRODUCTO.objects.all()
    form = FormClientesParaVenta()
    admin = User.objects.filter(username='Sra.Juanita')
    
    for juanita in admin:
        admin = juanita
    
   
    total = 0
    cliente = 0
    listaProductos = []
    cont = 0
    
    if request.method == 'POST':

        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        queryCliente = request.POST.get('cliente')
        
        if queryCliente != '':
        
            if usuario == str(admin):
                
                user = authenticate(request, username = usuario, password = contrasena)
                #se agrego el total asi que se corrio todo
                if user is not None:
                    contador = 0
                    for key,value in request.POST.items():
                        contador = contador + 1
                    
                    contador2 = 0
                    producto = []
                    for key,value in request.POST.items():

                        contador2 = contador2 +1

                        if contador2 == contador:
                            total = value

                        if contador2 > 1 and contador2 < contador -2:

                            if key == 'cliente':
                                cliente = value
                            
                            if contador2 > 2:
                                cont += 1
                                
                                producto.append(value)

                                if cont == 3:
                                    listaProductos.append(producto)
                                    producto = []
                                    cont = 0
                    
                    cliente = CLIENTE.objects.filter(id=cliente)
                    for client in cliente:
                        cliente = client

                    boleta = BOLETA.objects.create(
                        total_a_pagar = total,
                        usuario = usuarioBoleta,
                        cliente = cliente,
                        estado = 1
                    )
                    boleta.save()

                    bol = BOLETA.objects.all().last()
                    bol = BOLETA.objects.get(id = bol.id)

                    for listaP in listaProductos:
                        prod = PRODUCTO.objects.get(codigo_barra = listaP[0])
                    
                        detalleBoleta = DETALLE_BOLETA.objects.create(
                            boleta = bol,
                            cantidad = listaP[1],
                            monto_a_pagar = listaP[2],
                            producto = prod
                        )
                        detalleBoleta.save()

                    messages.warning(request, 'Venta realizada con exito')
                    return redirect('venta')
                    
                else:
                    messages.warning(request, 'Usuario o contraseña incorrectos')
            else:
                messages.warning(request, 'Usuario ingresado no es administrador')

        else:
            if request.method == 'POST':
                usuarioBoleta = request.user
                usuarioBoleta = User.objects.get(username=usuarioBoleta)
                contador = 0

                for key,value in request.POST.items():
                    contador = contador + 1
                
                contador2 = 0
                producto = []
                for key,value in request.POST.items():

                    contador2 = contador2 +1

                    if contador2 == contador:
                        total = value

                    if contador2 > 1 and contador2 < contador -2:

                        if contador2 > 2:
                            cont += 1
                            
                            producto.append(value)

                            if cont == 3:
                                listaProductos.append(producto)
                                producto = []
                                cont = 0
                
               

                boleta = BOLETA.objects.create(
                    total_a_pagar = total,
                    usuario = usuarioBoleta,
                    estado = 1
                )
                boleta.save()

                bol = BOLETA.objects.all().last()
                bol = BOLETA.objects.get(id = bol.id)

                for listaP in listaProductos:
                    prod = PRODUCTO.objects.get(codigo_barra = listaP[0])
                
                    detalleBoleta = DETALLE_BOLETA.objects.create(
                        boleta = bol,
                        cantidad = listaP[1],
                        monto_a_pagar = listaP[2],
                        producto = prod
                    )
                    detalleBoleta.save()

                messages.warning(request, 'Venta realizada con exito')
                return redirect('venta')
   
    return render(request, 'venta.html',{'productos':productos, 'form':form})

def RecepcionPedido(request, id = None):

    ordenPedido = ORDEN_PEDIDO.objects.all()
    detalleOrden = DETALLE_ORDEN.objects.all()

    ordenPedido2 = ""
    detalleOrden2 = ""
    if id:
        ordenPedido2 = ORDEN_PEDIDO.objects.filter(id=id)
        detalleOrden2 = DETALLE_ORDEN.objects.filter(orden_pedido=id)
    
    productos = PRODUCTO.objects.all()

    if request.method == 'POST':

        ordenPedido3 = ORDEN_PEDIDO.objects.get(id=id)
        validado = request.POST.get('validado')
        fecha = datetime.now().date()
        hora = datetime.now().time()
        print(fecha)
        print(hora)
        
        ordenPedido3.estado_recepcion = 1
        ordenPedido3.save()
        ordenPedido3.fecha_recepcion = fecha
        ordenPedido3.save()
        ordenPedido3.hora_recepcion = hora
        ordenPedido3.save()

        return redirect('RecepcionPedido')

    context= {
        'ordenPedido':ordenPedido,
        'productos':productos,
        'detalleOrden':detalleOrden,
        'ordenPedido2':ordenPedido2,
        'detalleOrden2':detalleOrden2
    }

    return render(request, 'recepcion_pedido.html',context)


##**************************Usuarios***************************************
@method_decorator(login_required, name='dispatch')
class UsuarioListado(ListView): 
    
    template_name = "usuarios/listar.html"
    model = User 
    # def get(self,request):

    #     usuarioSeg = request.user
    #     usuarioSeg = User.objects.get(username=usuarioSeg)

    #     seguimientoPag = SEGUIMIENTO_PAGINA.objects.create(
    #         pagina_visitada = "listar usuarios",
    #         usuario = usuarioSeg
    #     )
    #     seguimientoPag.save()
    #     return render(request, self.template_name)

    

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


@login_required(login_url="login")
def ProductoCrear(request):

    formProd = FormProducto(request.POST)
    formFam = FormFamiliaProd(request.POST)
    formProv = FormProductoProv(request.POST)
    nombre = request.POST.get('nombre')
    precio = request.POST.get('precio')
    precio_compra = request.POST.get('precio_compra')
    descripcion = request.POST.get('descripcion')
    stock = request.POST.get('stock')
    stock_critico = request.POST.get('stock_critico')
    proveedor = request.POST.get('proveedor')
    familia_producto = request.POST.get('familia_producto')
    fecha_vencimiento = request.POST.get('fecha_vencimiento')
    hora_vencimiento = request.POST.get('hora_vencimiento')
    tipo_producto = request.POST.get('tipo_producto')
    
    if request.method == 'POST':

        if (ValidacionCamposProducto(request,
            nombre, precio, descripcion, precio_compra, stock, stock_critico, proveedor, familia_producto, tipo_producto)
        ):
            if fecha_vencimiento:
                fecha_v = fecha_vencimiento[6:10] + '-' + fecha_vencimiento[3:5] + '-' + fecha_vencimiento[0:2] + ' ' + hora_vencimiento + ':00'
                fecha_vencimiento = fecha_vencimiento[0:2]+fecha_vencimiento[3:5]+fecha_vencimiento[6:10]
            else:
                fecha_v = "1000-10-10 00:00:00"
                fecha_vencimiento = "00000000"
                
            familia_producto = str(familia_producto).zfill(3)
            tipo_producto = str(tipo_producto).zfill(3)
            proveedor = str(proveedor).zfill(3)
            
            codigo_barra = proveedor + familia_producto + fecha_vencimiento + tipo_producto
            
            if familia_producto:
                familia_producto = FAMILIA_PRODUCTO.objects.filter(id = familia_producto)
            for famP in familia_producto:
                familia_producto = famP

            producto = PRODUCTO.objects.create(
                nombre = nombre.strip(),
                precio = precio.strip(),
                descripcion = descripcion.strip(),
                precio_compra = precio_compra.strip(),
                stock = stock.strip(),
                stock_critico = stock_critico.strip(),
                estado = 1,
                fecha_vencimiento = fecha_v,
                codigo_barra = codigo_barra,
                familia_producto = familia_producto
            )

            if producto is not None:
                producto.save()
                messages.warning(request, 'Producto creado correctamente')
                return redirect('listarProductos')
            else:
                messages.warning(request, 'No se pudo crear el Producto')

    return render(request, 'productos/crear.html',{'formProd':formProd, 'formFam':formFam, 'formProv':formProv})

@login_required(login_url="login")
def ProductoActualizar(request, id):

    producto = PRODUCTO.objects.get(id=id)
   
    form = FormProductoEdit(request.POST or None, instance=producto)
    formProd = FormProducto(request.POST or None, instance=producto)

    tipo_producto = len(producto.codigo_barra)
    tipo_producto = int(producto.codigo_barra[-3:tipo_producto])
    tipo_producto = TIPO_PRODUCTO.objects.get(id=tipo_producto)
    
    proveedor = int(producto.codigo_barra[0:3])
    proveedor = PROVEEDOR.objects.get(id=proveedor)
    
    fecha = str(producto.fecha_vencimiento)
    hora = str(producto.fecha_vencimiento)
    fecha = fecha[0:10]
    hora = hora[11:16]

    formFam = FormFamiliaProd(request.POST or None)
    formProv = FormProductoProv(request.POST or None)

    context = {
        'formProd':formProd, 
        'formFam':formFam, 
        'formProv':formProv, 
        'form':form,
        'tipo_producto':tipo_producto,
        'proveedor':proveedor,
        'fecha':fecha,
        'hora':hora
    }

    nombre = request.POST.get('nombre')
    precio = request.POST.get('precio')
    precio_compra = request.POST.get('precio_compra')
    descripcion = request.POST.get('descripcion')
    stock = request.POST.get('stock')
    stock_critico = request.POST.get('stock_critico')
    proveedor = request.POST.get('proveedor')
    familia_producto = request.POST.get('familia_producto')
    fecha_vencimiento = request.POST.get('fecha_vencimiento')
    hora_vencimiento = request.POST.get('hora_vencimiento')
    tipo_producto = request.POST.get('tipo_producto')

    if request.method == 'POST':
        if (ValidacionCamposProducto(request,
                nombre, precio, descripcion, precio_compra, stock, stock_critico, proveedor, familia_producto, tipo_producto)
            ):
                if fecha_vencimiento:
                    fecha_v = fecha_vencimiento[6:10] + '-' + fecha_vencimiento[3:5] + '-' + fecha_vencimiento[0:2] + ' ' + hora_vencimiento + ':00'
                    fecha_vencimiento = fecha_vencimiento[0:2]+fecha_vencimiento[3:5]+fecha_vencimiento[6:10]
                else:
                    fecha_v = "1000-10-10 00:00:00"
                    fecha_vencimiento = "00000000"
                    
                familia_producto = str(familia_producto).zfill(3)
                tipo_producto = str(tipo_producto).zfill(3)
                proveedor = str(proveedor).zfill(3)
                
                codigo_barra = proveedor + familia_producto + fecha_vencimiento + tipo_producto
                
                if familia_producto:
                    familia_producto = FAMILIA_PRODUCTO.objects.filter(id = familia_producto)
                for famP in familia_producto:
                    familia_producto = famP

                producto = PRODUCTO.objects.create(
                    nombre = nombre.strip(),
                    precio = precio.strip(),
                    descripcion = descripcion.strip(),
                    precio_compra = precio_compra.strip(),
                    stock = stock.strip(),
                    stock_critico = stock_critico.strip(),
                    estado = 1,
                    fecha_vencimiento = fecha_v,
                    codigo_barra = codigo_barra,
                    familia_producto = familia_producto
                )

                if producto is not None:
                    producto.save()
                    messages.warning(request, 'Producto creado correctamente')
                    return redirect('listarProductos')
                else:
                    messages.warning(request, 'No se pudo crear el Producto')


    return render(request, 'productos/actualizar.html',context)

def ValidacionCamposProducto(
    request,
    nombre, 
    precio, 
    descripcion, 
    precio_compra, 
    stock, 
    stock_critico,
    proveedor, 
    familia_producto, 
    tipo_producto
):
    estado = False
    nombre.strip()
    precio.strip()
    descripcion.strip()
    precio_compra.strip()
    stock.strip()
    stock_critico.strip()

    if len(nombre) < 3:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser mayor a 2')
    elif len(nombre) > 100:
        messages.warning(request, 'La cantidad de caracteres del nombre debe ser menor a 101')
    elif len(precio) < 1:
        messages.warning(request, 'La cantidad de caracteres del precio debe ser mayor a 0')
    elif len(precio) > 10:
        messages.warning(request, 'La cantidad de caracteres del precio debe ser menor a 11')
    elif len(descripcion) < 4:
        messages.warning(request, 'La cantidad de caracteres de la descripcion debe ser mayor a 3')
    elif len(descripcion) > 200:
        messages.warning(request, 'La cantidad de caracteres de la descripcion debe ser menor a 201')
    elif len(precio_compra) < 1:
        messages.warning(request, 'La cantidad de caracteres del precio de compra debe ser mayor a 0')
    elif len(precio_compra) > 10:
        messages.warning(request, 'La cantidad de caracteres del precio de compra debe ser menor a 11')
    elif len(stock) < 1:
        messages.warning(request, 'La cantidad de caracteres del stock debe ser mayor a 0')
    elif len(stock) > 10:
        messages.warning(request, 'La cantidad de caracteres del stock debe ser menor a 11')
    elif len(stock_critico) < 1:
        messages.warning(request, 'La cantidad de caracteres del stock critico debe ser mayor a 0')
    elif len(stock_critico) > 10:
        messages.warning(request, 'La cantidad de caracteres del stock critico debe ser menor a 11')
    elif len(proveedor) == 0:
        messages.warning(request, 'Se debe seleccionar al menos una opcion en proveedor')
    elif len(familia_producto) == 0:
        messages.warning(request, 'Se debe seleccionar al menos una opcion en familia de producto')
    elif len(tipo_producto) == 0:
         messages.warning(request, 'Se debe seleccionar al menos una opcion en tipo de producto')
    else:
        estado = True

    return estado

@method_decorator(login_required, name='dispatch')
class ProductoDetalle(DetailView):
    model = PRODUCTO


def DesactivarProducto(request, id):
    producto = PRODUCTO.objects.get(id = id)
    producto.estado = 0
    producto.save()
    messages.warning(request, f'Producto {producto.nombre} desactivado')
    return redirect('listarProductos')

def ActivarProducto(request, id):
    producto = PRODUCTO.objects.get(id = id)
    producto.estado = 1
    producto.save()
    messages.warning(request, f'Producto {producto.nombre} activado')
    return redirect('listarProductos')

##********************************************************************

##**************************Tipo de producto********************
@method_decorator(login_required, name='dispatch')
class TipoProductoListado(ListView):
    model = TIPO_PRODUCTO

@method_decorator(login_required, name='dispatch')
class TipoProductoCrear(SuccessMessageMixin, CreateView):
    model = TIPO_PRODUCTO
    form = TIPO_PRODUCTO
    fields = "__all__"
    success_message = 'Tipo producto creado correctamente'
    def get_success_url(self):
        return reverse('listarTiposProductos')

@method_decorator(login_required, name='dispatch')
class TipoProductoActualizar(SuccessMessageMixin, UpdateView):
    model = TIPO_PRODUCTO
    form = TIPO_PRODUCTO
    fields = "__all__"
    success_message = 'Familia producto correctamente'
    def get_success_url(self):
        return reverse('listarTiposProductos')

##******************************************************************

##**************************Familia de producto********************
@method_decorator(login_required, name='dispatch')
class FamiliaProductoListado(ListView):
    model = FAMILIA_PRODUCTO

@method_decorator(login_required, name='dispatch')
class FamiliaProductoCrear(SuccessMessageMixin, CreateView):
    model = FAMILIA_PRODUCTO
    form = FAMILIA_PRODUCTO
    fields = "__all__"
    success_message = 'Familia producto creado correctamente'

    def get_success_url(self):        
        return reverse('listarFamiliasProductos') # Redireccionamos a la vista principal 'leer'

@method_decorator(login_required, name='dispatch')
class FamiliaProductoActualizar(SuccessMessageMixin, UpdateView):
    model = FAMILIA_PRODUCTO
    form = FAMILIA_PRODUCTO
    fields = "__all__"
    success_message = 'Familia producto correctamente'
    def get_success_url(self):
        return reverse('listarFamiliasProductos')

##******************************************************************


##**************************Pedidos********************
@method_decorator(login_required, name='dispatch')
class PedidosListado(ListView):
    model = ORDEN_PEDIDO


def PedidosCrear(request, id = None):

    proveedores = PROVEEDOR.objects.all()

    tiposProductos = TIPO_PRODUCTO.objects.filter(proveedor=id)
    
    listaF = []
    for tiposP in tiposProductos:
        famId = FAMILIA_PRODUCTO.objects.filter(tipo_producto=tiposP)
        for f in famId:
            listaF.append(f.id)

    productos = PRODUCTO.objects.all()

    listaProds = [] 
    for prod in productos:
        idFam = FAMILIA_PRODUCTO.objects.filter(descripcion=prod.familia_producto)
        
        for idF in idFam:
            
            for listF in listaF:
                if listF == idF.id:
                    
                    listaProds.append(prod.nombre)

    if request.method == 'POST':

        listaProductos = []
        producto = []

        contador2 = 0
        for key,value in request.POST.items():
            contador2 += 1

        contador = 0
        fecha = ""
        cont = 0
        for key,value in request.POST.items():
            
            contador += 1
            
            if contador == 2:
                proveedorOrden = int(value)

            if contador > 2:
                
                if contador == contador2:
                    if value == "":
                        fecha = "1000-10-10"
                    else:
                        fecha = value
                        fecha = fecha[6:10]+ '-' +fecha[3:5]+ '-' + fecha[0:2]
                        print(fecha)

                if contador < contador2:
                    cont += 1
                    
                    producto.append(value)

                    if cont == 2:
                        listaProductos.append(producto)
                        producto = []
                        cont = 0

        

        proveedorOrden = PROVEEDOR.objects.get(id=proveedorOrden)
        print(proveedorOrden)

        ordenPedido = ORDEN_PEDIDO.objects.create(
            estado_recepcion = 0,
            proveedor = proveedorOrden,
            fecha_llegada = fecha
        )
        ordenPedido.save()

        ordenPedido = ORDEN_PEDIDO.objects.all().last()
        ordenPedido = ORDEN_PEDIDO.objects.get(id = ordenPedido.id)

        for listaP in listaProductos:
            prod = PRODUCTO.objects.get(nombre=listaP[0])

            detallePedido = DETALLE_ORDEN.objects.create(
                producto = prod,
                cantidad = listaP[1],
                orden_pedido = ordenPedido
            )
            detallePedido.save()
        
        messages.warning(request, 'Orden de pedido realizada con exito')
        return redirect('listarPedidos')

    
    context = {
        'proveedores':proveedores,
        'listaProds':listaProds
    }
    return render(request, 'pedidos/crear.html', context)

@login_required(login_url="login")
def PedidosDetalle(request, id):
    pedido = ORDEN_PEDIDO.objects.filter(id=id)
    detallesP = DETALLE_ORDEN.objects.filter(orden_pedido=id)
    context = {
        'pedido':pedido,
        'detallesP':detallesP,
        'id':id
    }
    return render(request, 'pedidos/detalles.html', context)

@method_decorator(login_required, name='dispatch')
class PedidosActualizar(SuccessMessageMixin, UpdateView):
    model = ORDEN_PEDIDO
    form = FormPedido()
    fields = "__all__"
    success_message = 'Pedido actualizado correctamente'
    def get_success_url(self):
        return reverse('listarPedidos')

def DesactivarPedido(request, id):
    pedido = ORDEN_PEDIDO.objects.get(id = id)
    pedido.estado_recepcion = 3
    pedido.save()
    messages.warning(request, f'Pedido {pedido.id} anulado')
    return redirect('listarPedidos')

def ActivarPedido(request, id):
    pedido = ORDEN_PEDIDO.objects.get(id = id)
    pedido.estado_recepcion = 0
    pedido.save()
    messages.warning(request, f'Pedido {pedido.id} activado')
    return redirect('listarPedidos')

##******************************************************************

##**************************Categoria proveedor**********************************
@login_required(login_url="login")
def CategoriasProvListar(request):

    categorias = CATEGORIA_PROVEEDOR.objects.all()

    return render(request, 'categoria_proveedor/listar.html', {'categorias':categorias})

@login_required(login_url="login")
def CategoriaProvCrear(request):

    if request.method == 'POST':

        categoria = request.POST.get('descripcion')

        categProv = CATEGORIA_PROVEEDOR.objects.create(
            descripcion = categoria
        )
        categProv.save()
        messages.warning(request, 'Categoria Proveedor creada con exito')
        return redirect('listarCategoriasProv')

    return render(request, 'categoria_proveedor/crear.html')

@login_required(login_url="login")
def CategoriaProvActualizar(request, id):
    
    categoriaProv = CATEGORIA_PROVEEDOR.objects.get(id=id)
    form = FormCategProv(request.POST or None, instance=categoriaProv)

    if request.method == 'POST':

        categoria = request.POST.get('descripcion')
        categoriaProv.descripcion = categoria
        categoriaProv.save()
        messages.warning(request, 'Categoria Proveedor actualizada con exito')
        return redirect('listarCategoriasProv')

    return render(request, 'categoria_proveedor/actualizar.html',{'form':form})
##******************************************************************

##**************************Boleta***************************************
@method_decorator(login_required, name='dispatch')
class BoletaListado(ListView):
    model = BOLETA

@login_required(login_url="login")
def BoletaDetalle(request, id):
    boleta = BOLETA.objects.filter(id=id)
    detalles = DETALLE_BOLETA.objects.filter(boleta=id)
    context = {
        'boleta':boleta,
        'detalles':detalles,
        'id':id
    }
    return render(request, 'boletas/detalles.html', context)

def DesactivarBoleta(request, id):
    boleta = BOLETA.objects.get(id = id)
    boleta.estado = 0
    boleta.save()
    messages.warning(request, f'Boleta {boleta.id} desactivado')
    return redirect('listarBoletas')

def ActivarBoleta(request, id):
    boleta = BOLETA.objects.get(id = id)
    boleta.estado = 1
    boleta.save()
    messages.warning(request, f'Boleta {boleta.id} activado')
    return redirect('listarBoletas')

##********************************************************************

##******************************Informes********************************
@login_required(login_url="login")
def CreacionInformes(request):

    formP = FormProducto()
    formT = FormFamiliaProd()
    formU = FormBoleta()
    formC = FormClientesParaVenta()
    formCliente = FormClientesInforme()
    formProveedor = FormProductoProv()
    formCatProv = FormProveedor()
    formProveeOrden = FormInformeOrdenPedido()
    FormSeg = FormSeguimientoPagina()

    listaProducto = []

    if request.method == 'POST':

        productos = request.POST.get('productos')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        nombre = request.POST.get('nombre')
        precioCompra = request.POST.get('precioCompra')
        stockCritico = request.POST.get('stockCritico')
        fechaVencimiento = request.POST.get('fechaVencimiento')
        codigoBarra = request.POST.get('codigoBarra')

        stock = request.POST.get('stock')
        stockCheck = request.POST.get('stockCheck')

        estado = request.POST.get('estado')
        estadoCheck = request.POST.get('estadoCheck')

        familiaProducto = request.POST.get('familiaProducto')
        familiaProductoCheck = request.POST.get('familiaProductoCheck')

        tipoProducto = request.POST.get('tipoProducto')
        tipoProductoCheck = request.POST.get('tipoProductoCheck')
        
        lista = []
        titulos = []
        # PRODUCTO.objects.filter().values_list("account__owner__code",)

        if productos == "on":

            ids = PRODUCTO.objects.all().values_list("id")
            titulos.append("ID")
            for valores in ids:
                valor = valores
                listaProducto.append(valor)
            lista.append(listaProducto)
            listaProducto = []

            if nombre == "on":
                valores = PRODUCTO.objects.all().values_list("nombre")
                titulos.append("NOMBRE")
                for valor in valores:
                    listaProducto.append(valor)
            lista.append(listaProducto)
            listaProducto = []

            if descripcion == "on":
                valores = PRODUCTO.objects.all().values_list("descripcion")
                titulos.append("DESCRIPCION")
                for valor in valores:
                    listaProducto.append(valor)
                lista.append(listaProducto)
                listaProducto = []

            if precio == "on":
                valores = PRODUCTO.objects.all().values_list("precio")
                titulos.append("PRECIO")
                for valor in valores:
                    listaProducto.append(valor)
                lista.append(listaProducto)
                listaProducto = []

            if precioCompra == "on":
                valores = PRODUCTO.objects.all().values_list("precio_compra")
                titulos.append("PRECIO DE COMPRA")
                for valor in valores:
                    listaProducto.append(valor)
                lista.append(listaProducto)
                listaProducto = []

            if stockCritico == "on":
                valores = PRODUCTO.objects.all().values_list("stock_critico")
                titulos.append("STOCK CRITICO")
                for valor in valores:
                    listaProducto.append(valor)
                lista.append(listaProducto)
                listaProducto = []

            if fechaVencimiento == "on":
                valores = PRODUCTO.objects.all().values_list("fecha_vencimiento")
                titulos.append("FECHA_VENCIMIENTO")
                for valor in valores:
                    listaProducto.append(valor)
                lista.append(listaProducto)
                listaProducto = []

            if codigoBarra == "on":
                valores = PRODUCTO.objects.all().values_list("codigo_barra")
                titulos.append("CODIGO_BARRA")
                for valor in valores:
                    listaProducto.append(valor)
                lista.append(listaProducto)
                listaProducto = []

            if stock == "on":
                print("algo")
                if stockCheck == "todos":
                    print("todos")
                elif stockCheck == "porNombre":
                    print("conStock")
                else:
                    print("sinStock")

            if estado == "on":
                print("algo")
                if estadoCheck == "todos":
                    print("todos")
                elif estadoCheck == "disponible":
                    print("disponible")
                else:
                    print("noDisponible")

            if familiaProducto == "on":
                print("algo")
                if familiaProductoCheck == "todosF":
                    print("todosF")
                else:
                    print("porNombreF")
                    familia_producto = request.POST.get('familia_producto')
                    print(familia_producto)
            
            if tipoProducto == "on":
                print("algo")
                if tipoProductoCheck == "todosT":
                    print("todosT")
                else:
                    print("porNombreT")
                    tipo_producto = request.POST.get('tipo_producto')
                    print(tipo_producto)

            print(lista)
            book_excel( lista, titulos)
            book_excel.book.save('productos.xlsx')
            



    # book = self.book_excel(holdings)

    # el archivo se guarda en memoria
    # with NamedTemporaryFile() as tmp:
    #     book.save(tmp.name)
    #     tmp.seek(0)
    #     stream = tmp.read()

    context = {
        'formP':formP,
        'formT':formT,
        'formU':formU,
        'formC':formC,
        'formCliente':formCliente,
        'formProveedor':formProveedor,
        'formCatProv':formCatProv,
        'formProveeOrden':formProveeOrden,
        'FormSeg':FormSeg
    }
    return render(request, 'informes.html', context)

def book_excel( datos, titulos):

    book = openpyxl.Workbook()  # Se crea un libro
    sheet = book.active  # Se activa la primera hoja

    # agrego los datos de la primera fila
    
    
    sheet.append(
        
        (
            datos,
        )
    )

    # recupero los datos de la query y luego los voy agregando por fila
    for h in datos:

        

        sheet.append(
            (
                "hola",
               
            )
        )
    return book
##********************************************************************

@login_required(login_url="login")

def CargaDatos(request):

    # # # # # # # # # cliente1 = CLIENTE.objects.create(
    # # # # # # # # #     run = "12326706-0",
    # # # # # # # # #     nombre = "Jose Palomo",
    # # # # # # # # #     telefono = "56914213464",
    # # # # # # # # #     correo = "jose.palomo.22@gmail.com",
    # # # # # # # # #     direccion = "San bernardo, Portales 15256",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente1.save()

    # # # # # # # # # cliente2 = CLIENTE.objects.create(
    # # # # # # # # #     run = "12413992-9",
    # # # # # # # # #     nombre = "Andrea Castillo",
    # # # # # # # # #     telefono = "56917489290",
    # # # # # # # # #     correo = "andre.cast.19@yahoo.com",
    # # # # # # # # #     direccion = "San bernardo, maestranza 1523",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente2.save()

    # # # # # # # # # cliente3 = CLIENTE.objects.create(
    # # # # # # # # #     run = "9455284-2",
    # # # # # # # # #     nombre = "Felipe Cordova",
    # # # # # # # # #     telefono = "56945031309",
    # # # # # # # # #     correo = "felipecor.va@outlook.com",
    # # # # # # # # #     direccion = "Santiago, lira 1444",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente3.save()

    # # # # # # # # # cliente4 = CLIENTE.objects.create(
    # # # # # # # # #     run = "18587107-k",
    # # # # # # # # #     nombre = "Andres Rodriguez",
    # # # # # # # # #     telefono = "56991802233",
    # # # # # # # # #     correo = "andre.roro@gmail.com",
    # # # # # # # # #     direccion = "Avenida Vicuña Mackenna, 439",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente4.save()

    # # # # # # # # # cliente5 = CLIENTE.objects.create(
    # # # # # # # # #     run = "6643850-3",
    # # # # # # # # #     nombre = "Joshua Carrillo",
    # # # # # # # # #     telefono = "56970002740",
    # # # # # # # # #     correo = "josh.carr_@gmail.com",
    # # # # # # # # #     direccion = "Calle Freire, 537",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente5.save()

    # # # # # # # # # cliente6 = CLIENTE.objects.create(
    # # # # # # # # #     run = "14748934-k",
    # # # # # # # # #     nombre = "Edward Norton",
    # # # # # # # # #     telefono = "56970864468",
    # # # # # # # # #     correo = "ed.norton@hotmail.com",
    # # # # # # # # #     direccion = "Avenida Providencia, 2653 - Of. 901",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente6.save()

    # # # # # # # # # cliente7 = CLIENTE.objects.create(
    # # # # # # # # #     run = "15945244-1",
    # # # # # # # # #     nombre = "Leonardo Pitt",
    # # # # # # # # #     telefono = "56908528619",
    # # # # # # # # #     correo = "leo@gmail.com",
    # # # # # # # # #     direccion = "Avenida Presidente Riesco, 5335 - Of. 925 Piso 9",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente7.save()

    # # # # # # # # # cliente8 = CLIENTE.objects.create(
    # # # # # # # # #     run = "16134207-6",
    # # # # # # # # #     nombre = "Brad Evans",
    # # # # # # # # #     telefono = "56932390401",
    # # # # # # # # #     correo = "brad@hotmail.com",
    # # # # # # # # #     direccion = "Calle Santo Domingo, 1160 - Of. 303",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente8.save()

    # # # # # # # # # cliente9 = CLIENTE.objects.create(
    # # # # # # # # #     run = "5945505-2",
    # # # # # # # # #     nombre = "Chris Pascal",
    # # # # # # # # #     telefono = "56986763759",
    # # # # # # # # #     correo = "chris_pascal@yahoo.com",
    # # # # # # # # #     direccion = "Calle Santos Dumont, 760",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente9.save()

    # # # # # # # # # cliente10 = CLIENTE.objects.create(
    # # # # # # # # #     run = "18251911-1",
    # # # # # # # # #     nombre = "Pedro Dicaprio",
    # # # # # # # # #     telefono = "56996056909",
    # # # # # # # # #     correo = "pedro_eldi@gmail.com",
    # # # # # # # # #     direccion = "Calle Marco Polo, 9038 - Loc.15",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente10.save()

    # # # # # # # # # cliente11 = CLIENTE.objects.create(
    # # # # # # # # #     run = "17749806-8",
    # # # # # # # # #     nombre = "Edgar Waltz",
    # # # # # # # # #     telefono = "56970764004",
    # # # # # # # # #     correo = "edg.altz@gmail.com",
    # # # # # # # # #     direccion = "Avenida Irarrazaval, 4888 - Of.202",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente11.save()

    # # # # # # # # # cliente12 = CLIENTE.objects.create(
    # # # # # # # # #     run = "16638053-7",
    # # # # # # # # #     nombre = "Angelina Lopez",
    # # # # # # # # #     telefono = "56945214880",
    # # # # # # # # #     correo = "angie_lo@yahoo.com",
    # # # # # # # # #     direccion = "Avenida Eliodoro Yañez, 1649 - Of. 805",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente12.save()

    # # # # # # # # # cliente13 = CLIENTE.objects.create(
    # # # # # # # # #     run = "22388500-4",
    # # # # # # # # #     nombre = "Jennifer Jolie",
    # # # # # # # # #     telefono = "56955285990",
    # # # # # # # # #     correo = "jenn_jo@gmail.com",
    # # # # # # # # #     direccion = "Avenida Providencia 2529 loc. 35, Providencia",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente13.save()

    # # # # # # # # # cliente14 = CLIENTE.objects.create(
    # # # # # # # # #     run = "13743818-6",
    # # # # # # # # #     nombre = "Keira Portman",
    # # # # # # # # #     telefono = "56980577654",
    # # # # # # # # #     correo = "k.port_@hotmail.com",
    # # # # # # # # #     direccion = "Calle Valdivieso, 45",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente14.save()

    # # # # # # # # # cliente15 = CLIENTE.objects.create(
    # # # # # # # # #     run = "6804734-k",
    # # # # # # # # #     nombre = "Natalie Knightley",
    # # # # # # # # #     telefono = "56965679100",
    # # # # # # # # #     correo = "nat_knightley@gmail.com",
    # # # # # # # # #     direccion = "Calle Juan De La Fuente, 0 - 027-a",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente15.save()

    # # # # # # # # # cliente16 = CLIENTE.objects.create(
    # # # # # # # # #     run = "16885911-2",
    # # # # # # # # #     nombre = "Kiernan Watson",
    # # # # # # # # #     telefono = "56998614242",
    # # # # # # # # #     correo = "kier.nan@gmail.com",
    # # # # # # # # #     direccion = "Avenida Peru, 8757",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente16.save()

    # # # # # # # # # cliente17 = CLIENTE.objects.create(
    # # # # # # # # #     run = "22019701-8",
    # # # # # # # # #     nombre = "Emma Shipka",
    # # # # # # # # #     telefono = "56931890958",
    # # # # # # # # #     correo = "emmshipka@gmail.com",
    # # # # # # # # #     direccion = "Calle Valdivieso, 45",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente17.save()

    # # # # # # # # # cliente18 = CLIENTE.objects.create(
    # # # # # # # # #     run = "11811887-1",
    # # # # # # # # #     nombre = "Andreina Borges",
    # # # # # # # # #     telefono = "56923139607",
    # # # # # # # # #     correo = "andre.borges_sr@gmail.com",
    # # # # # # # # #     direccion = "Calle Los Quillayes, 10757 - Parad.33",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente18.save()

    # # # # # # # # # cliente19 = CLIENTE.objects.create(
    # # # # # # # # #     run = "13066317-6",
    # # # # # # # # #     nombre = "George Gilmour",
    # # # # # # # # #     telefono = "56917777648",
    # # # # # # # # #     correo = "george.gilmour@yahoo.com",
    # # # # # # # # #     direccion = "Calle Merino Jarpa, 496 - Herradura Norte",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente19.save()

    # # # # # # # # # cliente20 = CLIENTE.objects.create(
    # # # # # # # # #     run = "22322272-2",
    # # # # # # # # #     nombre = "Dave Harrison",
    # # # # # # # # #     telefono = "56973356546",
    # # # # # # # # #     correo = "dave2harr@hotmail.com",
    # # # # # # # # #     direccion = "Calle Almirante Montt, 472",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente20.save()

    # # # # # # # # # cliente21 = CLIENTE.objects.create(
    # # # # # # # # #     run = "12297591-6",
    # # # # # # # # #     nombre = "Eric Page",
    # # # # # # # # #     telefono = "56987559327",
    # # # # # # # # #     correo = "eric.page@gmail.com",
    # # # # # # # # #     direccion = "Calle Lastra, 1209",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente21.save()

    # # # # # # # # # cliente22 = CLIENTE.objects.create(
    # # # # # # # # #     run = "23227346-1",
    # # # # # # # # #     nombre = "Jimmy Clapton",
    # # # # # # # # #     telefono = "56931404827",
    # # # # # # # # #     correo = "jim_clapton@outlook.com",
    # # # # # # # # #     direccion = "Calle Marco Polo, 9038 - Loc.15",
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # cliente22.save()

    # # # # # # # # # #CATEGORIA PROVEEDOR
    # # # # # # # # # categProv1 = CATEGORIA_PROVEEDOR.objects.create(
    # # # # # # # # #     descripcion = "BEBIDAS"
    # # # # # # # # # )
    # # # # # # # # # categProv1.save()

    # # # # # # # # # categProv2 = CATEGORIA_PROVEEDOR.objects.create(
    # # # # # # # # #     descripcion = "COMIDA Y DESPENSA"
    # # # # # # # # # )
    # # # # # # # # # categProv2.save()

    # # # # # # # # # categProv3 = CATEGORIA_PROVEEDOR.objects.create(
    # # # # # # # # #     descripcion = "DULCES Y SNACKS"
    # # # # # # # # # )
    # # # # # # # # # categProv3.save()

    # # # # # # # # # categProv4 = CATEGORIA_PROVEEDOR.objects.create(
    # # # # # # # # #     descripcion = "PRODUCTOS DE LIMPIEZA"
    # # # # # # # # # )
    # # # # # # # # # categProv4.save()

    # # # # # # # # # categProv5 = CATEGORIA_PROVEEDOR.objects.create(
    # # # # # # # # #     descripcion = "HIGIENE Y CUIDADOS"
    # # # # # # # # # )
    # # # # # # # # # categProv5.save()

    # # # # # # # # # categ1 = CATEGORIA_PROVEEDOR.objects.get(id=1)
    # # # # # # # # # categ2 = CATEGORIA_PROVEEDOR.objects.get(id=2)
    # # # # # # # # # categ3 = CATEGORIA_PROVEEDOR.objects.get(id=3)
    # # # # # # # # # categ4 = CATEGORIA_PROVEEDOR.objects.get(id=4)
    # # # # # # # # # categ5 = CATEGORIA_PROVEEDOR.objects.get(id=5)

    # # # # # # # # # #proveedores
    # # # # # # # # # proveedor1 = PROVEEDOR.objects.create(
    # # # # # # # # #     razon_social = "Coca-Cola Company",
    # # # # # # # # #     correo = "hernan_Danes@cocacola.cl",
    # # # # # # # # #     telefono = "800 21 99 99",
    # # # # # # # # #     direccion = "Av. Kennedy 5757 Piso 12, Torre Oriente, Las Condes, Santiago",
    # # # # # # # # #     categoria_proveedor = categ1,
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # proveedor1.save()

    # # # # # # # # # proveedor2 = PROVEEDOR.objects.create(
    # # # # # # # # #     razon_social = "Carozzi Corp",
    # # # # # # # # #     correo = "contacto.clientes@carozzi.cl",
    # # # # # # # # #     telefono = "800 321 111",
    # # # # # # # # #     direccion = "Avenida Longitudinal Sur 5201 KM. 23, San Bernardo, Santiago",
    # # # # # # # # #     categoria_proveedor = categ2,
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # proveedor2.save()

    # # # # # # # # # proveedor3 = PROVEEDOR.objects.create(
    # # # # # # # # #     razon_social = "Pepsico",
    # # # # # # # # #     correo = "consumidores.chile800@pepsico.com",
    # # # # # # # # #     telefono = "800-395 176",
    # # # # # # # # #     direccion = "PepsiCo Corporativo Avenida Kennedy 5454, piso 4. Las Condes, Santiago.",
    # # # # # # # # #     categoria_proveedor = categ3,
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # proveedor3.save()

    # # # # # # # # # proveedor4 = PROVEEDOR.objects.create(
    # # # # # # # # #     razon_social = "Colgate-Palmolive",
    # # # # # # # # #     correo = "servicios@colgate-palmolive.cl",
    # # # # # # # # #     telefono = "800 200 510",
    # # # # # # # # #     direccion = "Las Esteras Sur 2800, Quilicura, Region Metropolitana",
    # # # # # # # # #     categoria_proveedor = categ5,
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # proveedor4.save()

    # # # # # # # # # proveedor5 = PROVEEDOR.objects.create(
    # # # # # # # # #     razon_social = "Beiesdorf",
    # # # # # # # # #     correo = "Recepcion.Chile@beiersdorf.com",
    # # # # # # # # #     telefono = "56223688800",
    # # # # # # # # #     direccion = "Camino Lo Espejo 501, Maip�, Santiago, Chile.",
    # # # # # # # # #     categoria_proveedor = categ5,
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # proveedor5.save()

    # # # # # # # # # proveedor6 = PROVEEDOR.objects.create(
    # # # # # # # # #     razon_social = "Nestle",
    # # # # # # # # #     correo = "servicio.alcliente@nestle.cl",
    # # # # # # # # #     telefono = "9 4264 0564",
    # # # # # # # # #     direccion = "Carr Camino A Melipilla 15300, Maipu, Santiago, Region Metropolitana",
    # # # # # # # # #     categoria_proveedor = categ3,
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # proveedor6.save()

    # # # # # # # # # proveedor7 = PROVEEDOR.objects.create(
    # # # # # # # # #     razon_social = "Ideal",
    # # # # # # # # #     correo = "ventas.ideal@grupobimbo.com",
    # # # # # # # # #     telefono = "56959175002",
    # # # # # # # # #     direccion = "Av. Lo Espejo 02128, Lo Espejo, Region Metropolitana",
    # # # # # # # # #     categoria_proveedor = categ4,
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # proveedor7.save()

    # # # # # # # # # proveedor8 = PROVEEDOR.objects.create(
    # # # # # # # # #     razon_social = "Lider",
    # # # # # # # # #     correo = "servicioalcliente@lider.cl",
    # # # # # # # # #     telefono = "600 400 9000",
    # # # # # # # # #     direccion = "Av. Los Pajaritos 1790, Maip�, Regi�n Metropolitana",
    # # # # # # # # #     categoria_proveedor = categ2,
    # # # # # # # # #     estado = 1
    # # # # # # # # # )
    # # # # # # # # # proveedor8.save()


    # # # # # # # # # #tipo producto
    # # # # # # # # # prov1 = PROVEEDOR.objects.get(id=1)
    # # # # # # # # # prov2 = PROVEEDOR.objects.get(id=2)
    # # # # # # # # # prov3 = PROVEEDOR.objects.get(id=3)
    # # # # # # # # # prov4 = PROVEEDOR.objects.get(id=4)
    # # # # # # # # # prov5 = PROVEEDOR.objects.get(id=5)
    # # # # # # # # # prov6 = PROVEEDOR.objects.get(id=6)
    # # # # # # # # # prov7 = PROVEEDOR.objects.get(id=7)
    # # # # # # # # # prov8 = PROVEEDOR.objects.get(id=8)


    # # # # # # # # # tipoProd1 = TIPO_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Enlatados",
    # # # # # # # # #     proveedor = prov8
    # # # # # # # # # )
    # # # # # # # # # tipoProd1.save()

    # # # # # # # # # tipoProd2 = TIPO_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Granos",
    # # # # # # # # #     proveedor = prov2
    # # # # # # # # # )
    # # # # # # # # # tipoProd2.save()

    # # # # # # # # # tipoProd3 = TIPO_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Carnes",
    # # # # # # # # #     proveedor = prov5
    # # # # # # # # # )
    # # # # # # # # # tipoProd3.save()

    # # # # # # # # # tipoProd4 = TIPO_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Bebidas",
    # # # # # # # # #     proveedor = prov1
    # # # # # # # # # )
    # # # # # # # # # tipoProd4.save()

    # # # # # # # # # tipoProd5 = TIPO_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Dulces y Snacks",
    # # # # # # # # #     proveedor = prov3
    # # # # # # # # # )
    # # # # # # # # # tipoProd5.save()

    # # # # # # # # # tipoProd6 = TIPO_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Lacteos",
    # # # # # # # # #     proveedor = prov6
    # # # # # # # # # )
    # # # # # # # # # tipoProd6.save()

    # # # # # # # # # tipoProd7 = TIPO_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Panaderia y Pasteleria",
    # # # # # # # # #     proveedor = prov7
    # # # # # # # # # )
    # # # # # # # # # tipoProd7.save()

    # # # # # # # # # #familia producto
    # # # # # # # # # fam1 = TIPO_PRODUCTO.objects.get(id=1)
    # # # # # # # # # fam2 = TIPO_PRODUCTO.objects.get(id=2)
    # # # # # # # # # fam3 = TIPO_PRODUCTO.objects.get(id=3)
    # # # # # # # # # fam4 = TIPO_PRODUCTO.objects.get(id=4)
    # # # # # # # # # fam5 = TIPO_PRODUCTO.objects.get(id=5)
    # # # # # # # # # fam6 = TIPO_PRODUCTO.objects.get(id=6)
    # # # # # # # # # fam7 = TIPO_PRODUCTO.objects.get(id=7)

    # # # # # # # # # famProd1 = FAMILIA_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Atun",
    # # # # # # # # #     tipo_producto = fam1
    # # # # # # # # # )
    # # # # # # # # # famProd1.save()

    # # # # # # # # # famProd2 = FAMILIA_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Arroz",
    # # # # # # # # #     tipo_producto = fam2
    # # # # # # # # # )
    # # # # # # # # # famProd2.save()

    # # # # # # # # # famProd3 = FAMILIA_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Pollo",
    # # # # # # # # #     tipo_producto = fam3
    # # # # # # # # # )
    # # # # # # # # # famProd3.save()

    # # # # # # # # # famProd4 = FAMILIA_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Productos CocaCola",
    # # # # # # # # #     tipo_producto = fam4
    # # # # # # # # # )
    # # # # # # # # # famProd4.save()

    # # # # # # # # # famProd5 = FAMILIA_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Productos Pepsico",
    # # # # # # # # #     tipo_producto = fam5
    # # # # # # # # # )
    # # # # # # # # # famProd5.save()

    # # # # # # # # # famProd6 = FAMILIA_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Galletas Nestle",
    # # # # # # # # #     tipo_producto = fam5
    # # # # # # # # # )
    # # # # # # # # # famProd6.save()

    # # # # # # # # # famProd7 = FAMILIA_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Pan ideal",
    # # # # # # # # #     tipo_producto = fam7
    # # # # # # # # # )
    # # # # # # # # # famProd7.save()

    # # # # # # # # # famProd8 = FAMILIA_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Dulces Ideal",
    # # # # # # # # #     tipo_producto = fam5
    # # # # # # # # # )
    # # # # # # # # # famProd8.save()

    # # # # # # # # # famProd9 = FAMILIA_PRODUCTO.objects.create(
    # # # # # # # # #     descripcion = "Pastas",
    # # # # # # # # #     tipo_producto = fam2
    # # # # # # # # # )
    # # # # # # # # # famProd9.save()

    # #productos

    prod1 = FAMILIA_PRODUCTO.objects.get(id=1)
    prod2 = FAMILIA_PRODUCTO.objects.get(id=2)
    prod3 = FAMILIA_PRODUCTO.objects.get(id=3)
    prod4 = FAMILIA_PRODUCTO.objects.get(id=4)
    prod5 = FAMILIA_PRODUCTO.objects.get(id=5)
    prod6 = FAMILIA_PRODUCTO.objects.get(id=6)
    prod7 = FAMILIA_PRODUCTO.objects.get(id=7)
    prod8 = FAMILIA_PRODUCTO.objects.get(id=8)
    prod9 = FAMILIA_PRODUCTO.objects.get(id=9)

    # producto1 = PRODUCTO.objects.create(
    #     nombre = "Coca-Cola 3 litros",
    #     precio = 1300,
    #     descripcion = "Bebida fantasia Cocacola 3 litros",
    #     precio_compra = 900,
    #     stock = 50,
    #     stock_critico = 10,
    #     estado = 1,
    #     fecha_vencimiento = "2022/12/29 12:00:00",
    #     codigo_barra = "100429122022004",
    #     familia_producto = prod4
    # )
    # producto1.save()

    # # # # # producto2 = PRODUCTO.objects.create(
    # # # # #     nombre = "Papas Chips Lays Pepsico",
    # # # # #     precio = 1000,
    # # # # #     descripcion = "Bolsa de Chips lays",
    # # # # #     precio_compra = 750,
    # # # # #     stock = 20,
    # # # # #     stock_critico = 5,
    # # # # #     estado = 1,
    # # # # #     fecha_vencimiento = "2022/12/29 12:00:00",
    # # # # #     codigo_barra = "300529122022005",
    # # # # #     familia_producto = prod5
    # # # # # )
    # # # # # producto2.save()
    
    # # # # # producto3 = PRODUCTO.objects.create(
    # # # # #     nombre = "Nuggets de pollo Lider",
    # # # # #     precio = 2300,
    # # # # #     descripcion = "Bolsa de nuggets",
    # # # # #     precio_compra = 1700,
    # # # # #     stock = 10,
    # # # # #     stock_critico = 3,
    # # # # #     estado = 1,
    # # # # #     fecha_vencimiento = "2022/12/29 12:00:00",
    # # # # #     codigo_barra = "800329122022003",
    # # # # #     familia_producto = prod3
    # # # # # )
    # # # # # producto3.save()

    # # # # # producto4 = PRODUCTO.objects.create(
    # # # # #     nombre = "Galletas Triton x4 Nestle",
    # # # # #     precio = 300,
    # # # # #     descripcion = "Galletas Triton 4un",
    # # # # #     precio_compra = 200,
    # # # # #     stock = 50,
    # # # # #     stock_critico = 10,
    # # # # #     estado = 1,
    # # # # #     fecha_vencimiento = "2022/12/29 12:00:00",
    # # # # #     codigo_barra = "600529122022005",
    # # # # #     familia_producto = prod6
    # # # # # )
    # # # # # producto4.save()

    # # # # # producto5 = PRODUCTO.objects.create(
    # # # # #     nombre = "Pepsi 3 litros",
    # # # # #     precio = 1300,
    # # # # #     descripcion = "Bebida Pepsi 3 litros",
    # # # # #     precio_compra = 850,
    # # # # #     stock = 30,
    # # # # #     stock_critico = 10,
    # # # # #     estado = 1,
    # # # # #     fecha_vencimiento = "2022/12/29 12:00:00",
    # # # # #     codigo_barra = "300529122022005",
    # # # # #     familia_producto = prod5
    # # # # # )
    # # # # # producto5.save()

    # # # # # producto6 = PRODUCTO.objects.create(
    # # # # #     nombre = "Rallita de vainilla Marinela",
    # # # # #     precio = 1200,
    # # # # #     descripcion = "Rayita crema sabor vainilla",
    # # # # #     precio_compra = 900,
    # # # # #     stock = 50,
    # # # # #     stock_critico = 10,
    # # # # #     estado = 1,
    # # # # #     fecha_vencimiento = "2022/12/29 12:00:00",
    # # # # #     codigo_barra = "700829122022005",
    # # # # #     familia_producto = prod8
    # # # # # )
    # # # # # producto6.save()

    # # # # # producto7 = PRODUCTO.objects.create(
    # # # # #     nombre = "Pinguinos x6 un Marinela",
    # # # # #     precio = 1300,
    # # # # #     descripcion = "Pack de 6un Pinguinos",
    # # # # #     precio_compra = 1000,
    # # # # #     stock = 30,
    # # # # #     stock_critico = 5,
    # # # # #     estado = 1,
    # # # # #     fecha_vencimiento = "2022/12/28 12:00:00",
    # # # # #     codigo_barra = "700828122022005",
    # # # # #     familia_producto = prod8
    # # # # # )
    # # # # # producto7.save()

    # # # # # producto8 = PRODUCTO.objects.create(
    # # # # #     nombre = "Rayita frutilla Marinela",
    # # # # #     precio = 1200,
    # # # # #     descripcion = "Rayita crema sabor frutilla",
    # # # # #     precio_compra = 900,
    # # # # #     stock = 30,
    # # # # #     stock_critico = 10,
    # # # # #     estado = 1,
    # # # # #     fecha_vencimiento = "2022/12/27 12:00:00",
    # # # # #     codigo_barra = "700827122022005",
    # # # # #     familia_producto = prod8
    # # # # # )
    # # # # # producto8.save()

    # # # # # producto9 = PRODUCTO.objects.create(
    # # # # #     nombre = "Tortillas Rapiditas 8un Ideal",
    # # # # #     precio = 1000,
    # # # # #     descripcion = "Pack 8 un 200g Tortillas",
    # # # # #     precio_compra = 9850,
    # # # # #     stock = 20,
    # # # # #     stock_critico = 5,
    # # # # #     estado = 1,
    # # # # #     fecha_vencimiento = "2022/12/29 12:00:00",
    # # # # #     codigo_barra = "700729122022007",
    # # # # #     familia_producto = prod7
    # # # # # )
    # # # # # producto9.save()

    producto10 = PRODUCTO.objects.create(
        nombre = "Atun lomito en agua Lider",
        precio = 1300,
        descripcion = "Lata de atun",
        precio_compra = 1090,
        stock = 20,
        stock_critico = 10,
        estado = 1,
        fecha_vencimiento = "2022-12-29 12:00:00",
        codigo_barra = "800129122022001",
        familia_producto = prod1
    )
    producto10.save()

    producto11 = PRODUCTO.objects.create(
        nombre = "Arroz Pregraneado 1kg Lider",
        precio = 1300,
        descripcion = "Paquete de arroz pregraneado 1kg",
        precio_compra = 1160,
        stock = 20,
        stock_critico = 5,
        estado = 1,
        fecha_vencimiento = "2022-12-22 12:00:00",
        codigo_barra = "800229122022002",
        familia_producto = prod2
    )
    producto11.save()

    producto12 = PRODUCTO.objects.create(
        nombre = "Arroz 1kg Lider",
        precio = 1000,
        descripcion = "Paquete de 1kg arroz lider",
        precio_compra = 890,
        stock = 20,
        stock_critico = 5,
        estado = 1,
        fecha_vencimiento = "2022-12-30 12:00:00",
        codigo_barra = "800230122022002",
        familia_producto = prod2
    )
    producto12.save()

    producto13 = PRODUCTO.objects.create(
        nombre = "Pasta 400g tallarines Carozzi",
        precio = 600,
        descripcion = "Paquete de 400g de tallarines",
        precio_compra = 490,
        stock = 20,
        stock_critico = 5,
        estado = 1,
        fecha_vencimiento = "2022-12-29 12:00:00",
        codigo_barra = "200929122022003",
        familia_producto = prod9
    )
    producto13.save()

    producto14 = PRODUCTO.objects.create(
        nombre = "Pasta 400g spaghetti Carozzi",
        precio = 590,
        descripcion = "Paquete de 400g de spaghetti",
        precio_compra = 440,
        stock = 20,
        stock_critico = 5,
        estado = 1,
        fecha_vencimiento = "2022-12-30 12:00:00",
        codigo_barra = "200930122022002",
        familia_producto = prod9
    )
    producto14.save()

    producto15 = PRODUCTO.objects.create(
        nombre = "Pasta 400g quifaros Carozzi",
        precio = 600,
        descripcion = "Paquete de 400g de quifaros",
        precio_compra = 490,
        stock = 20,
        stock_critico = 5,
        estado = 1,
        fecha_vencimiento = "2022-12-28 12:00:00",
        codigo_barra = "200928122022002",
        familia_producto = prod4
    )
    producto15.save()

    producto16 = PRODUCTO.objects.create(
        nombre = "Coca-Cola 1.5 litros",
        precio = 700,
        descripcion = "Bebida de 1.5 litros coca-cola",
        precio_compra = 590,
        stock = 15,
        stock_critico = 3,
        estado = 1,
        fecha_vencimiento = "2022-12-28 12:00:00",
        codigo_barra = "100428122022004",
        familia_producto = prod4
    )
    producto16.save()

    producto17 = PRODUCTO.objects.create(
        nombre = "Fanta Naranja 3 litros",
        precio = 1290,
        descripcion = "Bebida 3 litros sabor naranja",
        precio_compra = 900,
        stock = 20,
        stock_critico = 5,
        estado = 1,
        fecha_vencimiento = "2022-12-30 12:00:00",
        codigo_barra = "100430122022004",
        familia_producto = prod4
    )
    producto17.save()

    producto18 = PRODUCTO.objects.create(
        nombre = "Agua 6.5 litros Benedictino",
        precio = 1600,
        descripcion = "Agua Benedictino 6.5 litros",
        precio_compra = 1400,
        stock = 10,
        stock_critico = 2,
        estado = 1,
        fecha_vencimiento = "2023-12-29 12:00:00",
        codigo_barra = "100429122023004",
        familia_producto = prod4
    )
    producto18.save()

    producto19 = PRODUCTO.objects.create(
        nombre = "Agua 1.5 litros Benedictino",
        precio = 800,
        descripcion = "Agua Benedictino 1.5 litros",
        precio_compra = 600,
        stock = 20,
        stock_critico = 5,
        estado = 1,
        fecha_vencimiento = "2023-12-28 12:00:00",
        codigo_barra = "100428122023004",
        familia_producto = prod4
    )
    producto19.save()

    producto20 = PRODUCTO.objects.create(
        nombre = "Galletas Triton Limon x4 Nestle",
        precio = 300,
        descripcion = "Galletas Triton sabor limon 4un",
        precio_compra = 200,
        stock = 20,
        stock_critico = 5,
        estado = 1,
        fecha_vencimiento = "2022-12-30 12:00:00",
        codigo_barra = "600530122022005",
        familia_producto = prod6
    )
    producto20.save()

    # ##pago fiados
    # pagoFiado1 = PAGO_FIADO.objects.create(
    #     estado = 1,
    #     monto = 1500,
    #     fecha = "12-06-2021",
    #     fecha_final = "29-06-2021"
    # )
    # pagoFiado1.save()

    # pagoFiado2 = PAGO_FIADO.objects.create(
    #     estado = 1,
    #     monto = 3500,
    #     fecha = "20-06-2021",
    #     fecha_final = "12-07-2021"
    # )
    # pagoFiado2.save()

    # pagoFiado3 = PAGO_FIADO.objects.create(
    #     estado = 1,
    #     monto = 6500,
    #     fecha = "04-07-2021",
    #     fecha_final = "21-07-2021"
    # )
    # pagoFiado3.save()

    # pagoFiado4 = PAGO_FIADO.objects.create(
    #     estado = 1,
    #     monto = 2500,
    #     fecha = "05-07-2021",
    #     fecha_final = "25-07-2021"
    # )
    # pagoFiado4.save()

    # ##detalle fiado
    # cli1 = CLIENTE.objects.get(id=1)
    # cli2 = CLIENTE.objects.get(id=2)
    # cli3 = CLIENTE.objects.get(id=3)
    # cli4 = CLIENTE.objects.get(id=4)
    # pag1 = PAGO_FIADO.objects.get(id=1)
    # pag2 = PAGO_FIADO.objects.get(id=2)
    # pag3 = PAGO_FIADO.objects.get(id=3)
    # pag4 = PAGO_FIADO.objects.get(id=4)

    # detPagoFiado1 = DETALLE_FIADO.objects.create(
    #     monto_abonado = 1500,
    #     pago_fiado = pag1,
    #     fecha_abono = "23-06-2021",
    #     cliente = cli1
    # )
    # detPagoFiado1.save()

    # detPagoFiado2 = DETALLE_FIADO.objects.create(
    #     monto_abonado = 3000,
    #     pago_fiado = pag2,
    #     fecha_abono = "21-06-2021",
    #     cliente = cli2
    # )
    # detPagoFiado2.save()

    # detPagoFiado3 = DETALLE_FIADO.objects.create(
    #     monto_abonado = 500,
    #     pago_fiado = pag3,
    #     fecha_abono = "22-06-2021",
    #     cliente = cli2
    # )
    # detPagoFiado3.save()

    # detPagoFiado4 = DETALLE_FIADO.objects.create(
    #     monto_abonado = 5000,
    #     pago_fiado = pag4,
    #     fecha_abono = "07-07-2021",
    #     cliente = cli3
    # )
    # detPagoFiado4.save()

    # detPagoFiado5 = DETALLE_FIADO.objects.create(
    #     monto_abonado = 2500,
    #     pago_fiado = pag4,
    #     fecha_abono = "27-07-2021",
    #     cliente = cli1
    # )
    # detPagoFiado5.save()

    # # # # ##orden pedido
    # # # # pagoFiado1 = ORDEN_PEDIDO.objects.create(
    # # # #     estado_recepcion = 1,
    # # # #     proveedor = 1,
    # # # #     fecha_pedido = "01-07-2021",
    # # # #     fecha_llegada = "11-07-2021",
    # # # #     fecha_recepcion = "25-07-2021",
    # # # #     hora_recepcion = "12:00:00"
    # # # # )
    # # # # pagoFiado1.save()

    # # # # pagoFiado2 = ORDEN_PEDIDO.objects.create(
    # # # #     estado_recepcion = 1,
    # # # #     proveedor = 2,
    # # # #     fecha_pedido = "01-08-2021",
    # # # #     fecha_llegada = "14-08-2021",
    # # # #     fecha_recepcion = "18-08-2021",
    # # # #     hora_recepcion = "12:00:00"
    # # # # )
    # # # # pagoFiado2.save()

    # # # # pagoFiado3 = ORDEN_PEDIDO.objects.create(
    # # # #     estado_recepcion = 1,
    # # # #     proveedor = 3,
    # # # #     fecha_pedido = "01-12-2021",
    # # # #     fecha_llegada = "07-12-2021",
    # # # #     fecha_recepcion = "09-12-2021",
    # # # #     hora_recepcion = "12:00:00"
    # # # # )
    # # # # pagoFiado3.save()

    # # # # pagoFiado4 = ORDEN_PEDIDO.objects.create(
    # # # #     estado_recepcion = 4,
    # # # #     proveedor = 1,
    # # # #     fecha_pedido = "01-12-2021",
    # # # #     fecha_llegada = "04-12-2021",
    # # # #     fecha_recepcion = "16-12-2021",
    # # # #     hora_recepcion = "12:00:00"
    # # # # )
    # # # # pagoFiado4.save()

    # # # # pagoFiado5 = ORDEN_PEDIDO.objects.create(
    # # # #     estado_recepcion = 2,
    # # # #     proveedor = 1,
    # # # #     fecha_pedido = "01-11-2021",
    # # # #     fecha_llegada = "03-10-2021",
    # # # #     fecha_recepcion = "09-10-2021",
    # # # #     hora_recepcion = "12:00:00"
    # # # # )
    # # # # pagoFiado5.save()

    # # # # ##detalle orden
    # # # # detalleOrden = DETALLE_ORDEN.objects.create(
    # # # #     cantidad = 2,
    # # # #     orden_pedido = 1,
    # # # #     producto = 1,
    # # # # )
    # # # # detalleOrden.save()

    # # # # detalleOrden = DETALLE_ORDEN.objects.create(
    # # # #     cantidad = 2,
    # # # #     orden_pedido = 1,
    # # # #     producto = 1,
    # # # # )
    # # # # detalleOrden.save()

    # # # # detalleOrden = DETALLE_ORDEN.objects.create(
    # # # #     cantidad = 2,
    # # # #     orden_pedido = 1,
    # # # #     producto = 1,
    # # # # )
    # # # # detalleOrden.save()

    # # # # detalleOrden = DETALLE_ORDEN.objects.create(
    # # # #     cantidad = 2,
    # # # #     orden_pedido = 1,
    # # # #     producto = 1,
    # # # # )
    # # # # detalleOrden.save()

    # # # # detalleOrden = DETALLE_ORDEN.objects.create(
    # # # #     cantidad = 2,
    # # # #     orden_pedido = 1,
    # # # #     producto = 1,
    # # # # )
    # # # # detalleOrden.save()
        
    

    return render(request, 'carga.html')