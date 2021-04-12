
from django.contrib import admin
from django.urls import path
from src import views, static
from src.views import Index
from src.views import UsuarioListado, UsuarioDetalle, UsuarioCrear, UsuarioActualizar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Ingreso, name="ingreso"),
    path('index/', views.Index, name="index"),
    # path('registroUsuarios/', views.RegistroUsuarios, name="registroUsuarios"),
    # path('ingresar/', views.Ingresar, name="ingresar"),

        # **************************************Usuario
    # La ruta 'leer' en donde listamos todos los registros o postres de la Base de Datos
    path('usuarios/', UsuarioListado.as_view(template_name = "usuarios/listar.html"), name='listarUsuarios'),
 
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
]
