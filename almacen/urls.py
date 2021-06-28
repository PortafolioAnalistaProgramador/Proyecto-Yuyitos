
from django.contrib import admin
from django.urls import path
from src import views, static
from src.views import Index
from src.views import UsuarioListado, UsuarioDetalle, UsuarioCrear, UsuarioActualizar, DesactivarUsuario, ActivarUsuario
from src.views import ClienteListado, ClienteCrear, ClienteDetalle, ClienteActualizar, DesactivarCliente, ActivarCliente
from src.views import ProveedorListado, ProveedorCrear, ProveedorDetalle, ProveedorActualizar, DesactivarProveedor, ActivarProveedor
from src.views import ProductoListado, ProductoCrear, ProductoDetalle, ProductoActualizar
from src.views import PedidosListado, PedidosCrear, PedidosDetalle, PedidosActualizar, DesactivarPedido, ActivarPedido
from src.views import BoletaListado, DesactivarBoleta, ActivarBoleta, BoletaDetalle
from src.views import TipoProductoActualizar, TipoProductoListado, TipoProductoCrear
from src.views import FamiliaProductoListado, FamiliaProductoActualizar, FamiliaProductoCrear
from src.views import CategoriaProvActualizar, CategoriaProvCrear, CategoriasProvListar
from src.views import CreacionInformesProductos, CreacionInformesBoletas, CreacionInformesClientes, CreacionInformesFiados, CreacionInformesProveedores, CreacionInformesPedidos
from src.views import PagosFiadosListado, DesactivarPagoFiado, ActivarPagoFiado
# from src.views import book_excel
from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.conf import settings

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', views.Login, name="login"),
    path('index/', views.Index, name="index"),
    path('venta/', views.Venta, name="venta"),
    path('recepcion/', views.RecepcionPedido, name="RecepcionPedido"),
    path('recepcion/<int:id>', views.RecepcionPedido, name="RecepcionPedido"),
    path('pagar_fiado/', views.PagarFiado, name="PagarFiadoTodos"),
    path('pagar_fiado/<int:id>', views.PagarFiado, name="PagarFiado"),

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
    path('usuarios/', views.UsuarioListado, name='listarUsuarios'),
 
    path('usuarios/detalle/<int:id>', views.UsuarioDetalle, name='detalles'),
    
    path('usuarios/crear/', views.UsuarioCrear, name="crearUsuario"),

    path('usuarios/editar/<int:id>', views.UsuarioActualizar, name="actualizarUsuario"),
    
    path('usuarios/desactivarUsuario/<int:id>', views.DesactivarUsuario, name="desactivarUsuario"),
    path('usuarios/activarUsuario/<int:id>', views.ActivarUsuario, name="activarUsuario"), 
    # # **************************************


    # **************************************Cliente
    path('clientes/', views.ClienteListado, name='listarClientes'),
 
    path('clientes/crear/', views.ClienteCrear, name="crearCliente"),
 
    path('clientes/detalle/<int:id>', views.ClienteDetalle, name='detalles'),

    path('clientes/editar/<int:id>', views.ClienteActualizar, name="editarCliente"),
    
    path('clientes/desactivarCliente/<int:id>', views.DesactivarCliente, name="desactivarCliente"),
    path('clientes/activarCliente/<int:id>', views.ActivarCliente, name="activarCliente"), 
    
    # # **************************************


    # **************************************Proveedor
    path('proveedores/', views.ProveedorListado, name='listarProveedores'),
    
    path('proveedores/crear/', views.ProveedorCrear, name="crearProveedor"),
 
    path('proveedores/detalle/<int:id>', views.ProveedorDetalle, name='detalles'),
    
    path('proveedores/editar/<int:id>', views.ProveedorActualizar, name="actualizarProveedor"),
    # path('proveedores/editar/<int:pk>', ProveedorActualizar.as_view(template_name = "proveedores/actualizar.html"), name='actualizar'), 
    
    path('proveedores/desactivarProveedor/<int:id>', views.DesactivarProveedor, name="desactivarProveedor"),
    path('proveedores/activarProveedor/<int:id>', views.ActivarProveedor, name="activarProveedor"),
    # # **************************************

    # **************************************Proveedor
    path('productos/', views.ProductoListado, name='listarProductos'),
    
    path('productos/crear/', views.ProductoCrear, name="crearProducto"),
    # path('productos/crear/', ProductoCrear.as_view(template_name = "productos/crear.html"), name='crearProducto'),
 
    path('productos/detalle/<int:id>', views.ProductoDetalle, name='detalles'),

    # path('productos/editar/<int:pk>', ProductoActualizar.as_view(template_name = "productos/actualizar.html"), name='actualizar'), 
    path('productos/editar/<int:id>', views.ProductoActualizar, name="actualizarProducto"),
    
    path('productos/desactivarProducto/<int:id>', views.DesactivarProducto, name="desactivarProducto"),
    path('productos/activarProducto/<int:id>', views.ActivarProducto, name="activarProducto"),
    # # **************************************

    # **********************************************Pedidos*********************************************************************
    path('pedidos/', views.PedidosListado, name='listarPedidos'),
 
    # path('pedidos/crear/', PedidosCrear.as_view(template_name = "pedidos/crear.html"), name='crearPedido'),
    path('pedidos/crear/', views.PedidosCrear, name="crearPedido"),
    path('pedidos/crear/<int:id>', views.PedidosCrear, name="crearPedido"),
    
    path('pedidos/detalle/<int:id>', views.PedidosDetalle, name="detallePedido"),

    path('pedidos/editar/<int:id>', PedidosActualizar.as_view(template_name = "pedidos/actualizar.html"), name='actualizar'), 
    
    path('pedidos/desactivarPedido/<int:id>', views.DesactivarPedido, name="desactivarPedido"),
    path('pedidos/activarPedido/<int:id>', views.ActivarPedido, name="activarPedido"),
    # # **************************************************************************************************************************


    # **********************************************Boletas*********************************************************************
    path('boletas/', BoletaListado.as_view(template_name = "boletas/listar.html"), name='listarBoletas'),

    path('boletas/detalle/<int:id>', views.BoletaDetalle, name="detallesBoleta"),

    path('boletas/desactivarBoleta/<int:id>', views.DesactivarBoleta, name="desactivarBoleta"),
    path('boletas/activarBoleta/<int:id>', views.ActivarBoleta, name="activarBoleta"),
    # # **************************************************************************************************************************

    # **********************************************TipoProductos*********************************************************************
    path('tipos_productos/', views.TipoProductoListado, name='listarTiposProductos'),
 
    path('tipos_productos/crear/', TipoProductoCrear.as_view(template_name = "tipos_productos/crear.html"), name='crearTipoProducto'),
 
    # path('tipos_productos/detalle/<int:pk>', PedidosDetalle.as_view(template_name = "pedidos/detalles.html"), name='detalles'),

    path('tipos_productos/editar/<int:pk>', TipoProductoActualizar.as_view(template_name = "tipos_productos/actualizar.html"), name='actualizarTipoProducto'), 
    # # **************************************************************************************************************************

    # **********************************************TipoProductos*********************************************************************
    path('familias_productos/', views.FamiliaProductoListado, name='listarFamiliasProductos'),
 
    path('familias_productos/crear/', FamiliaProductoCrear.as_view(template_name = "familia_producto/crear.html"), name='crearFamiliaProducto'),
 
    # path('tipos_productos/detalle/<int:pk>', PedidosDetalle.as_view(template_name = "pedidos/detalles.html"), name='detalles'),

    path('familias_productos/editar/<int:pk>', FamiliaProductoActualizar.as_view(template_name = "familia_producto/actualizar.html"), name='actualizarFamiliaProducto'), 
    # # **************************************************************************************************************************

    ##*********************************categoria proveedor**************************
    path('categoria_proveedor/', views.CategoriasProvListar, name="listarCategoriasProv"),
    path('categoria_proveedor/crear/', views.CategoriaProvCrear, name="crearCategoriaProv"),
    path('categoria_proveedor/editar/<int:id>', views.CategoriaProvActualizar, name="actualizarCategoriaProv"),
    ##*****************************************************************************
   

    ##*******************************Informes****************************************
    path('informesProductos/', views.CreacionInformesProductos, name="informesProductos"),
    path('informesBoletas/', views.CreacionInformesBoletas, name="informesBoletas"),
    path('informesClientes/', views.CreacionInformesClientes, name="informesClientes"),
    path('informesFiados/', views.CreacionInformesFiados, name="informesFiados"),
    path('informesProveedores/', views.CreacionInformesProveedores, name="informesProveedores"),
    path('informesPedidos/', views.CreacionInformesPedidos, name="informesPedidos"),
    
    ##******************************************************************************

    # **********************************************TipoProductos*********************************************************************
    path('fiados/', views.PagosFiadosListado, name='pagoFiadosListar'),
    path('fiados/desactivarPagoFiado/<int:id>', views.DesactivarPagoFiado, name="desactivarPagoFiado"),
    path('fiados/activarPagoFiado/<int:id>', views.ActivarPagoFiado, name="activarPagoFiado"),
 
    # path('familias_productos/crear/', FamiliaProductoCrear.as_view(template_name = "familia_producto/crear.html"), name='crearFamiliaProducto'),
 
    # path('tipos_productos/detalle/<int:pk>', PedidosDetalle.as_view(template_name = "pedidos/detalles.html"), name='detalles'),

    # path('familias_productos/editar/<int:pk>', FamiliaProductoActualizar.as_view(template_name = "familia_producto/actualizar.html"), name='actualizarFamiliaProducto'), 
    # # **************************************************************************************************************************

]

