#CoWorkSpace
Esta API permite gestionar reservas de espacios de coworking, permitiendo a los usuarios registrarse, autenticarse, consultar disponibilidad y administrar sus reservas bajo ciertas condiciones.

###Modelos:
Entre los modelos presentes en el aplicativo tenemos:

###Espacio:
Reservacion:

###Inicializacion:
Para iniciar el aplicativo es necesario ejecutar el siguiente comando para construir los contenedores
docker-compose build

Luego ejecutar el siguiente comando, para iniciar los servicios 
docker-compose up -d

###Pruebas unitarias:
Se realizaron pruebas unitarias para verificar la funcionalidad de cada una las vistas, revisar ciertas restricciones, ademas de comprobar las respuestas del servidor. Para ejecutar las pruebas unitarias es necesario ejecutar los siguientes comandos para cada uno de los modelos
docker-compose exec djangapp pytest User/test/test_user.py
docker-compose exec djangapp pytest Spaces/tests/test_reservation.py
docker-compose exec djangapp pytest Spaces/tests/test_space.py
