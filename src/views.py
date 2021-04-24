from django.shortcuts import render, redirect
from .models import USUARIO, CLIENTE
from django.contrib import messages
from django import forms
from src.forms import FormRegistro, FormCliente
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin 
from django.urls import reverse

# def Ingreso(request):
#     usuario = request.POST.get('usuario')
#     contrasena = request.POST.get('contrasena')

#     if request.method == 'POST':

#         if USUARIO.objects.filter(usuario=usuario) and USUARIO.objects.filter(contrasena=contrasena):
#             return redirect('/index/')
#         else:
#             messages.warning(request, 'Usuario o contraseña incorrectos')    
#     return render(request, 'usuarios/ingreso.html')

def Ingreso(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    if request.method == 'POST':
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('index/')
        else:
            messages.warning(request, 'Usuario o contraseña incorrectos')
        
    return render(request, 'usuarios/ingreso.html')


def Index(request):
    return render(request, 'index.html')

# def RegistroUsuarios(request):
#     form = FormRegistro()
#     email = request.POST.get('email')
#     validarEmail = User.objects.filter(email = email)

    
#     if request.method == 'POST':
#         if validarEmail:
#             messages.warning(request, 'el email ya existe')
#         else:
#             form = FormRegistro(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('index/')
    
#     form.fields['username'].help_text = None
#     form.fields['password1'].help_text = None
#     form.fields['password2'].help_text = None
#     return render(request, 'usuarios/registroUsuarios.html',{'form':form})


##*****************************Usuarios**************************************
class UsuarioListado(ListView): 
    model = User 
 
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

def UsuarioActualizar(request, id):

    user = User.objects.get(id=id)
    form = FormRegistro(request.POST or None, instance=user)
    
    if form.is_valid():
        
        form.save()
        messages.warning(request, 'Usuario editado correctamente')
        return redirect('listarUsuarios')
    
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    return render(request, 'usuarios/actualizar.html',{'form':form})

class UsuarioDetalle(DetailView): 
    model = User 
##*************************************************************************

##**************************Clientes***************************************
class ClienteListado(ListView):
    model = CLIENTE

class ClienteCrear(SuccessMessageMixin, CreateView, ListView):
    model = CLIENTE
    form = FormCliente()
    fields = "__all__"
    success_message = 'Cliente creado correctamente'

    def get_success_url(self):
        return reverse('listarClientes')

class ClienteDetalle(DetailView):
    model = CLIENTE

class ClienteActualizar(SuccessMessageMixin, UpdateView):
    model = CLIENTE
    form = FormCliente()
    fields = "__all__"
    success_message = 'Cliente actualizado correctamente'
    def get_success_url(self):
        return reverse('listarClientes')

##******************************************************************