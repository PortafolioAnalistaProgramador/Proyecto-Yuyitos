from django.forms.widgets import DateInput
from django.http.response import ResponseHeaders
from django.shortcuts import render, redirect
from .models import CLIENTE, PROVEEDOR, PRODUCTO, ORDEN_PEDIDO
from django.contrib import messages
from django import forms
import csv
import datetime
import xlwt

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum

from src.forms import FormRegistro, FormCliente, FormProveedor, FormProducto, FormPedidos

from django.http import JsonResponse, HttpResponse
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


def Calendar(request):
    return render(request, 'calendario.html')


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

    form = FormRegistro()
    email = request.POST.get('email')
    validarEmail = User.objects.filter(email = email)
    
    
    if request.method == 'POST':
        if validarEmail:
            messages.warning(request, 'el email ya existe')
        else:
            form = FormRegistro(request.POST)
            if form.is_valid():
                form.save()
                messages.warning(request, 'Usuario creado correctamente')
                return redirect('listarUsuarios')
    
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    return render(request, 'usuarios/crear.html',{'form':form})

@login_required(login_url="ingreso")
def UsuarioActualizar(request, id):

    user = User.objects.get(id=id)

    if request.method == 'POST':
        form = FormRegistro(request.POST, instance=user)

        if form.is_valid():
            
            form.save()
            messages.warning(request, 'Usuario editado correctamente')
            return redirect('listarUsuarios')
    
    # form.fields['username'].help_text = None
    # form.fields['password1'].help_text = None
    # form.fields['password2'].help_text = None

    return render(request, 'usuarios/actualizar.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class UsuarioDetalle(DetailView): 
    model = User 
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
##********************************************************************
##********************************************************************
##**************************Pedidos********************


##**************************Pedidos********************
@method_decorator(login_required, name='dispatch')
class PedidosListado(ListView):
    model = ORDEN_PEDIDO

@method_decorator(login_required, name='dispatch')
class PedidosCrear(SuccessMessageMixin, CreateView, ListView):
    model = ORDEN_PEDIDO
    form = FormPedidos()
    fields = "__all__"
    success_message = 'Pedido creado correctamente'

    def get_success_url(self):
        return reverse('listarPedidos')

@method_decorator(login_required, name='dispatch')
class PedidosDetalle(DetailView):
    model = ORDEN_PEDIDO

@method_decorator(login_required, name='dispatch')
class PedidosActualizar(SuccessMessageMixin, UpdateView):
    model = ORDEN_PEDIDO
    form = FormPedidos()
    fields = "__all__"
    success_message = 'Pedido actualizado correctamente'
    def get_success_url(self):
        return reverse('listarPedidos')

##******************************************************************

##******************************************************************
##***************Pendiente el metodo actualizar  y crear************
##**************************Recepcion de pedidos********************
@method_decorator(login_required, name='dispatch')
class RegistroPedidosListado(ListView):
    model = ORDEN_PEDIDO

@method_decorator(login_required, name='dispatch')
class RegistroPedidosDetalle(DetailView):
    model = ORDEN_PEDIDO

def export_csv(request):

    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=registro pedidos'+ \
        str(datetime.datetime.now())+'.csv'

    writer=csv.writer(response)
    writer.writerow(['estado_recepcion','proveedor','fecha_pedido','fecha_llegada','fecha_recepcion','hora_recepcion'])

    PEDIDOS = ORDEN_PEDIDO.objects.filter()

    for PEDIDOS in ORDEN_PEDIDO:
        writer.writerow([ORDEN_PEDIDO.estado_recepcion,ORDEN_PEDIDO.proveedor,
                        ORDEN_PEDIDO.fecha_pedido,ORDEN_PEDIDO.fecha_llegada, 
                        ORDEN_PEDIDO.fecha_recepcion, ORDEN_PEDIDO.hora_recepcion])

    return response
    
##******************************************************************************************
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] ='attachment; filename=registro pedidos' + \
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('templates')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['estado_recepcion','proveedor','fecha_pedido','fecha_llegada','fecha_recepcion','hora_recepcion']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style  = xlwt.XFStyle()

    rows = ORDEN_PEDIDO.objects.filter().values_list('estado_recepcion','proveedor','fecha_pedido','fecha_llegada','fecha_recepcion','hora_recepcion')

    for row in rows:
        row_num +=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]),font_style)
    wb.save(response)

    return response


##******************************************************************************************
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] ='inline; attachment; filename=registro pedidos' + \
        str(datetime.datetime.now())+'.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    html_string=render_to_string(
        'registro pedidos/pdf_output.html',{'registro pedidos':[] ,'total':0})
    html=HTML(string=html_string)

    result=html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output=open(output.name, 'rb')
        response.write(output.read())

    return response




    # ucci sector 2 31
    # estable lo dieron vuelta, sentado
    # esta estable
    # 



