
from rest_framework.test import APITestCase
from Users.models import CustomUser
from Spaces.models import Space, Reservation
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta


# Pruebas generales para reservaciones
class ReservationAPITestCase(APITestCase):
    
    # Configuracion inicial
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username="testuser1", password="password2", email="username1@gmail.com")    
        self.user2 = CustomUser.objects.create_user(username="testuser2", password="password2", email="username2@gmail.com")    

        self.space1 = Space.objects.create(name="Sala A", available=False)
        self.space2 = Space.objects.create(name="Sala B", available=False)
        self.space3 = Space.objects.create(name="Sala C", available=False)
        self.space4 = Space.objects.create(name="Sala D", available=False)
        self.space5 = Space.objects.create(name="Sala E", available=False)

        self.reservation1 = Reservation.objects.create(
            space=self.space1,
            start_time = timezone.make_aware(datetime(2025, 3, 14, 0, 0, 0)),
            end_time = timezone.make_aware(datetime(2025, 3, 15, 0, 0, 0)) ,
            user=self.user1
        )
        
        self.reservation2 = Reservation.objects.create(
            space=self.space2,
            start_time = timezone.make_aware(datetime(2025, 3, 20, 0, 0, 0)),
            end_time = timezone.make_aware(datetime(2025, 3, 22, 0, 0, 0)) ,
            user=self.user1
        )
        
        self.reservation3 = Reservation.objects.create(
            space=self.space3,
            start_time = timezone.make_aware(datetime(2025, 3, 20, 0, 0, 0)),
            end_time = timezone.make_aware(datetime(2025, 3, 24, 0, 0, 0)) ,
            user=self.user2
        )
    
    
    # ==================================================
    # PRUEBAS DE AUTENTICACION
    # ==================================================
    
    def test_unauthenticated_user(self):
        
        response1 = self.client.post(reverse("reservations_list_create"), {})
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response2 = self.client.get(reverse("reservations_list_create"))
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
            
        response3 = self.client.delete(reverse('reservation_delete', kwargs={'id': 1}))
        self.assertEqual(response3.status_code, status.HTTP_401_UNAUTHORIZED)
          
    
    # ==================================================
    # PRUEBAS DE LISTADO Y CREACION DE RESERVACIONES
    # ==================================================

    
    # Prueba para obtener reservaciones del usuario autenticado
    def test_list_reservation_user1(self):
        self.client.force_authenticate(user=self.user1) 
        response1 = self.client.get(reverse("reservations_list_create"))        
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 2)                     
        self.client.logout()

    def test_list_reservation_user2(self):
        self.client.force_authenticate(user=self.user2) 
        response1 = self.client.get(reverse("reservations_list_create"))        
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data), 1)                     
        self.client.logout()
        
    
    # Prueba para crear reservaciones
    def test_create_reservation(self):
        self.client.force_authenticate(user=self.user2)             
        reservation_data = {
            "space": self.space1.id,
            "start_time": timezone.now() + timedelta(hours=2),
            "end_time": timezone.now() + timedelta(hours=3)
        }
        
        response = self.client.post(reverse("reservations_list_create"), reservation_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user2.id)
    
    
    # Prueba para crear reservaciones con datos ausentes
    def test_create_reservation_wrong_data(self):
        self.client.force_authenticate(user=self.user2)             
        reservation_data1 = {
            "space": 9999,
            "start_time": timezone.now() + timedelta(hours=2),
            "end_time": timezone.now() + timedelta(hours=3)
        }
        
        response1 = self.client.post(reverse("reservations_list_create"), reservation_data1, format="json")
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("space", response1.data) 
        
        reservation_data2 = {
            "start_time": timezone.now() + timedelta(hours=2),
            "end_time": timezone.now() + timedelta(hours=3)
        }
        
        response2 = self.client.post(reverse("reservations_list_create"), reservation_data2, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("space", response2.data) 
        
        
        reservation_data3 = {
            "space": self.space1.id,
        }
        
        response3 = self.client.post(reverse("reservations_list_create"), reservation_data3, format="json")
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("start_time", response3.data)
        self.assertIn("end_time", response3.data)

        
    # Prueba para cancelar reservacion
    def test_delete_reservation(self):
        self.client.force_authenticate(user=self.user2)         
        self.test_reservation = Reservation.objects.create(
            space=self.space4,
            start_time=timezone.now() + timedelta(hours=4), 
            end_time=timezone.now() + timedelta(hours=5),
            user=self.user2
        )
        
        response = self.client.delete(reverse('reservation_delete', kwargs={'id': self.test_reservation.id}))  
        self.space4.refresh_from_db()        
        self.test_reservation.refresh_from_db()
              
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.space4.available) 
        self.assertFalse(self.test_reservation.is_active) 
        
        self.client.logout()
    
    
    # Prueba para cancelar reservacion con menos de una 1 hora de anticipacion
    def test_delete_reservation_hour(self):
        self.client.force_authenticate(user=self.user2)         
        self.test_reservation = Reservation.objects.create(
            space=self.space4,
            start_time=timezone.now() + timedelta(minutes=30), 
            end_time=timezone.now() + timedelta(hours=5),
            user=self.user2
        )
        
        response = self.client.delete(reverse('reservation_delete', kwargs={'id': self.test_reservation.id}))  
        self.space4.refresh_from_db()        
        self.test_reservation.refresh_from_db()
              
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)           
        self.client.logout()

    
    # Prueba para cancelar reservacion que no es del usuario
    def test_delete_reservation_wrong_user(self):
        self.client.force_authenticate(user=self.user2)           
        response = self.client.delete(reverse('reservation_delete', kwargs={'id': self.reservation2.id}))                
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)           
        self.client.logout()        