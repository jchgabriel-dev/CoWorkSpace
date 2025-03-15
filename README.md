<h1>CoWorkSpace</h1>
Esta API permite gestionar reservas de espacios de coworking, permitiendo a los usuarios registrarse, autenticarse, consultar disponibilidad y administrar sus reservas bajo ciertas condiciones.

<h2>Tecnologias usadas:</h2>

* Django Rest Framework (DRF)
* Docker
* PostgreSQL
* JWT 

  
<h2>Modelos:</h2>
Entre los modelos presentes en el aplicativo tenemos:

* Usuario: Son los usuarios registrados en el sistema, cuentan con un nombre de usuario, contraseña y correo electronico.
* Espacio: Son los espacios que los usuarios pueden reservar, cuenta con campos para la ubicación, descripción y capacidad, además de un campo para verificar si están disponibles o no.
* Reservación: Son las reservaciones que hace cada uno de los usuarios, están relacionados respectivamente con sus usuarios creadores y el espacio seleccionado, además de contar con fechas para el inicio y fin de la reservación.

<h2>Funcionalidades:</h2>
<h3>Autenticación</h3>

* POST /register → Registro un usuario, pasando como parámetros el nombre de usuarios, contraseña y correo electrónico.
* POST /login → Inicio de sesión y generación de token, siendo necesario el nombre de usuario y la contraseña.

<h3>Espacios</h3>

* GET /spaces → Regresa un listado de los espacios disponibles. 
* GET /spaces/:id → Regresa el detalle de un espacio específico pasando como parámetro el identificador. 
* GET /reservations/available?date=YYYY-MM-DD → Consulta la disponibilidad de los espacios, considerando las reservaciones registradas, verificando que en dicha fecha no esté bajo una reservación cada uno de los espacios.

<h3>Reservaciones</h3>

* GET /reservations → Regresa un listado de las reservaciones pertenecientes al usuario autenticado. 
* POST /reservations → Creación de una nueva reservación, registrando automáticamente el usuario autenticado como el dueño.
* DELETE /reservations/:id → Permite cancelar una reservación, siempre que sea con una 1 hora de anticipación.


<h2>Inicializacion:</h2>

Para iniciar el aplicativo es necesario ejecutar el siguiente comando para construir los contenedores.
```
docker-compose build
```

Luego ejecutar el siguiente comando, para iniciar los servicios.

```
docker-compose up -d
```

<h2>Pruebas unitarias:</h2>
Se realizaron pruebas unitarias para verificar la funcionalidad de cada una las vistas, revisar ciertas restricciones, ademas de comprobar las respuestas del servidor. Para ejecutar las pruebas unitarias es necesario ejecutar los siguientes comandos para cada uno de los modelos.

```
docker-compose exec djangapp pytest User/test/test_user.py
docker-compose exec djangapp pytest Spaces/tests/test_reservation.py
docker-compose exec djangapp pytest Spaces/tests/test_space.py
```
