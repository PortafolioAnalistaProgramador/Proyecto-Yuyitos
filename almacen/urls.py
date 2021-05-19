
from django.contrib import admin
from django.urls import path
from src import views, static
from src.views import Index, export_csv
from src.views import UsuarioListado, UsuarioDetalle, UsuarioCrear, UsuarioActualizar
from src.views import ClienteListado, ClienteCrear, ClienteDetalle, ClienteActualizar
from src.views import ProveedorListado, ProveedorCrear, ProveedorDetalle, ProveedorActualizar
from src.views import ProductoListado, ProductoCrear, ProductoDetalle, ProductoActualizar
from src.views import PedidosListado, PedidosCrear, PedidosDetalle, PedidosActualizar
from src.views import RegistroPedidosDetalle, RegistroPedidosListado

import csv


from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.conf import settings

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', views.Login, name="login"),
    path('index/', views.Index, name="index"),
    # path('registroUsuarios/', views.RegistroUsuarios, name="registroUsuarios"),
    # path('ingresar/', views.Ingresar, name="ingresar"),

    #******************************Restaurar contrasena
    path('reset_password/', 
        PasswordResetView.as_view(template_name="accounts/password_reset.html",email_template_name="accounts/password_reset_email.html"), name="reset_password"),
    path('reset_password_sent/', 
        PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', 
        PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    #**************************************************

    # **************************************Usuario
    # La ruta 'leer' en donde listamos todos los registros o postres de la Base de Datos
    path('usuarios/', UsuarioListado.as_view(), name='listarUsuarios'),
 
    # # La ruta 'detalles' en donde mostraremos una página con los detalles de un postre o registro 
    path('usuarios/detalle/<int:pk>', UsuarioDetalle.as_view(template_name = "usuarios/detalles.html"), name='detalles'),
 
    # # La ruta 'crear' en donde mostraremos un formulario para crear un nuevo postre o registro  
    #  path('usuarioAdmin/crear/', UsuarioCrear.as_view(template_name = "administrar_usuarios/crear.html"), name='crear'),
    path('usuarios/crear/', views.UsuarioCrear, name="crearUsuario"),
    # # La ruta 'actualizar' en donde mostraremos un formulario para actualizar un postre o registro de la Base de Datos 
    path('usuarios/editar/<int:id>', views.UsuarioActualizar, name="actualizarUsuario"),
 
    # # La ruta 'eliminar' que usaremos para eliminar un postre o registro de la Base de Datos 
    #  path('usuarioAdmin/eliminar/<int:pk>', UsuarioEliminar.as_view(), name='eliminar'),    
    # # **************************************


    # **************************************Cliente
    path('clientes/', ClienteListado.as_view(template_name = "clientes/listar.html"), name='listarClientes'),
 
    path('clientes/crear/', ClienteCrear.as_view(template_name = "clientes/crear.html"), name='crearCliente'),
 
    path('clientes/detalle/<int:pk>', ClienteDetalle.as_view(template_name = "clientes/detalles.html"), name='detalles'),

    path('clientes/editar/<int:pk>', ClienteActualizar.as_view(template_name = "clientes/actualizar.html"), name='actualizar'), 
    # # **************************************


    # **************************************Proveedor
    path('proveedores/', ProveedorListado.as_view(template_name = "proveedores/listar.html"), name='listarProveedores'),
 
    path('proveedores/crear/', ProveedorCrear.as_view(template_name = "proveedores/crear.html"), name='crearProveedor'),
 
    path('proveedores/detalle/<int:pk>', ProveedorDetalle.as_view(template_name = "proveedores/detalles.html"), name='detalles'),

    path('proveedores/editar/<int:pk>', ProveedorActualizar.as_view(template_name = "proveedores/actualizar.html"), name='actualizar'), 
    # # **************************************

    # **************************************Proveedor
    path('productos/', ProductoListado.as_view(template_name = "productos/listar.html"), name='listarProductos'),
 
    path('productos/crear/', ProductoCrear.as_view(template_name = "productos/crear.html"), name='crearProducto'),
 
    path('productos/detalle/<int:pk>', ProductoDetalle.as_view(template_name = "productos/detalles.html"), name='detalles'),

    path('productos/editar/<int:pk>', ProductoActualizar.as_view(template_name = "productos/actualizar.html"), name='actualizar'), 
    # # **************************************

    # **************************************Pedidos
    path('pedidos/', PedidosListado.as_view(template_name = "pedidos/listar.html"), name='listarPedidos'),
    
    path('pedidos/crear/', PedidosCrear.as_view(template_name = "pedidos/crear.html"), name='crearPedidos'),
 
    path('pedidos/detalle/<int:pk>', PedidosDetalle.as_view(template_name = "pedidos/detalles.html"), name='detalles'),

    path('pedidos/editar/<int:pk>', PedidosActualizar.as_view(template_name = "pedidos/actualizar.html"), name='actualizar'), 
    
     # **************************************Registro de pedidos

    path('registro pedidos/', RegistroPedidosListado.as_view(template_name = "registro pedidos/listar.html"), name='listarRegistroPedidos'),
    
    path('registro pedidos/detalle/<int:pk>', RegistroPedidosDetalle.as_view(template_name = "registro pedidos/detalles.html"), name='detalles'),


    path('export_csv', views.export_csv,
        name="export-csv"),

    path('export_excel', views.export_excel,
        name="export-excel"),

    path('export_pdf', views.export_pdf,
        name="export-pdf"),


    # # **************************************
]

