
from rest_framework.test import APITestCase
from Users.models import CustomUser
from Spaces.models import Space, Reservation
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta

# Pruebas generales para reservaciones
class UserAPITestCase(APITestCase):
    
    # Configuracion inicial
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username="testuser1", password="password1", email="username1@gmail.com")    
        self.user2 = CustomUser.objects.create_user(username="testuser2", password="password2", email="username2@gmail.com")    
        

    # Prueba para registrar usuarios con datos ausentes
    def test_register_wrong_data(self):
        user_data1 = {
            "username": "testuser3",
        }
        
        response1 = self.client.post(reverse("register"), user_data1, format="json")
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response1.data)
        self.assertIn("email", response1.data)
    
    
    # Prueba para login con datos incorrectos
    def test_login_wrong_data(self):
        user_data1 = {
            "username": "testuser1",
            "password": "wrong"
        }
        response = self.client.post(reverse('login'), user_data1, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Credenciales invalidas")
    
    
    # Prueba para login con datos incorrectos
    def test_login_right_data(self):
        user_data1 = {
            "username": "testuser1",
            "password": "password1"
        }
        response = self.client.post(reverse('login'), user_data1, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
