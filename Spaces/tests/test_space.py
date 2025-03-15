
from rest_framework.test import APITestCase
from Users.models import CustomUser
from Spaces.models import Space, Reservation
import datetime
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import datetime 


# Pruebas generales para espacio
class SpaceAPITestCase(APITestCase):
    
    # Configuracion inicial
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password")    
        self.client.force_authenticate(user=self.user) 
        
        self.space1 = Space.objects.create(name="Sala A", available=True)
        self.space2 = Space.objects.create(name="Sala B", available=True)
        self.space3 = Space.objects.create(name="Sala C", available=False)
        
        self.reservation = Reservation.objects.create(
            space=self.space3,
            start_time = timezone.make_aware(datetime(2025, 3, 20, 0, 0, 0)),
            end_time = timezone.make_aware(datetime(2025, 3, 20, 1, 0, 0)) ,
            user=self.user
        )
    
    # ==================================================
    # PRUEBAS DE AUTENTICACION
    # ==================================================
    
    def test_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse("spaces_available"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.get(reverse("spaces_detail", kwargs={"pk": self.space1.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
          
    
    # ==================================================
    # PRUEBAS DE LISTADO DE ESPACIOS DISPONIBLES
    # ==================================================    
    
    # Prueba para verificar la cantidad de espacios disponibles
    def test_get_available_spaces(self):
        response = self.client.get(reverse("spaces_available"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)     
       
       
    # Prueba para obtener solo los espacios disponibles
    def test_get_only_available_spaces(self):
        response = self.client.get(reverse("spaces_available"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for space in response.data:
            self.assertTrue(space["available"])
    
    # Prueba para obtener un listado vacio
    def test_no_spaces_available(self):
        Space.objects.all().delete()
        response = self.client.get(reverse("spaces_available"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    
    # ==================================================
    # PRUEBAS DE DETALLE DE ESPACIO
    # ==================================================
    
    # Prueba para obtener un espacio especifico
    def test_get_existing_space(self):
        response = self.client.get(reverse("spaces_detail", kwargs={"pk": self.space1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.space1.name)
    
    # Prueba para obtener un espacio inexistente
    def test_get_nonexistent_space(self):
        response = self.client.get(reverse("spaces_detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

        

# Pruebas para obtener espacios disponibles segun una fecha
class SpaceDateAvailableAPITestCase(APITestCase):
    
    # Configuracion inicial
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password")    
        self.client.force_authenticate(user=self.user) 
        
        self.space1 = Space.objects.create(name="Sala A", available=True)
        self.space2 = Space.objects.create(name="Sala B", available=True)
        self.space3 = Space.objects.create(name="Sala C", available=False)
        self.space4 = Space.objects.create(name="Sala D", available=False)
        self.space5 = Space.objects.create(name="Sala E", available=False)

        self.reservation = Reservation.objects.create(
            space=self.space3,
            start_time = timezone.make_aware(datetime(2025, 3, 14, 0, 0, 0)),
            end_time = timezone.make_aware(datetime(2025, 3, 15, 0, 0, 0)) ,
            user=self.user
        )
        
        self.reservation = Reservation.objects.create(
            space=self.space4,
            start_time = timezone.make_aware(datetime(2025, 3, 20, 0, 0, 0)),
            end_time = timezone.make_aware(datetime(2025, 3, 22, 0, 0, 0)) ,
            user=self.user
        )
        
        self.reservation = Reservation.objects.create(
            space=self.space5,
            start_time = timezone.make_aware(datetime(2025, 3, 20, 0, 0, 0)),
            end_time = timezone.make_aware(datetime(2025, 3, 24, 0, 0, 0)) ,
            user=self.user
        )
    

        self.test_date1 = datetime(2025, 3, 14).date()
        self.test_date2 = datetime(2025, 3, 21).date()
        self.test_date3 = datetime(2025, 3, 23).date()

    
    # Prueba de parametro de fecha con formato incorrecto   
    def test_invalid_date_format(self):
        response = self.client.get(reverse("spaces_available_date"), {"date": "invalid-date"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Formato de fecha inválido.")
        
        
    # Prueba de parametro de fecha faltante   
    def test_missing_date(self):
        response = self.client.get(reverse("spaces_available_date"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "El parámetro 'date' es requerido.")
                        
    
    # Prueba con fecha 1
    def test_get_available_spaces_date_1(self):
        response = self.client.get(reverse("spaces_available_date"), {"date": self.test_date1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['spaces_available']), 4)     


    # Prueba con fecha 2
    def test_get_available_spaces_date_2(self):
        response = self.client.get(reverse("spaces_available_date"), {"date": self.test_date2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['spaces_available']), 3)  
        
    # Prueba con fecha 3
    def test_get_available_spaces_date_3(self):
        response = self.client.get(reverse("spaces_available_date"), {"date": self.test_date3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['spaces_available']), 4)  