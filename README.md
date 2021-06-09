# Proyecto-Yuyitos
Sistema de administracion de un almacen

Para la correcta ejecucion del proyecto, necesitara instalar y crear algunas cosas, favor de seguir las instrucciones.
antes de comenzar favor de instalar Python version 3 y Django version 3.

1.- una vez descargado el proyecto ingrese a la ruta Proyecto_Yuyitos/my_env/bin y ejecutar el archivo activate desde el teminal o desde 
linea de comandos dependiendo del sistema operativo que use.

2.- una vez activado el entorno virtual ejecutar los siguientes comandos si esta en Windows

pip install django-extensions

pip instal cx-Oracle

si esta desde distrubuciones de ubuntu solo ejecutar el primero.

3.- Luego desde SqlDeveloper ejecutar en el usuario principal los siguientes comandos, esto funcionara si tiene una version de oracle desde 12c para arriba:

CREATE USER "C##JUANITA" IDENTIFIED BY "123456";

GRANT CONNECT TO "C##JUANITA";

GRANT RESOURCE TO "C##JUANITA";

ALTER USER C##JUANITA quota 100M on USERS;

4.- Una vez creado el usuario, migraremos el modelo desde el proyecto, nos ubicaremos en la ruta Proyecto_Yuyitos/almacen y ejecutaremos los siguientes 
comandos por separados desde el terminal:

python manage.py makemigrations

python manage.py migrate

5.- ahora podemos proceder a ejecutar el script en sqldeveloper, el archivo tiene por nombre inserciones.sql

si el archivo llegase a fallar, favor de ejecutar por partes, por ejemplo, un grupo de inserciones hasta el commit y luego los siguientes grupos.

7.- Por ultimo ya podemos ejecutar el servidor del proyecto con el siguiente comando desde el terminal:

python manage.py runserver
