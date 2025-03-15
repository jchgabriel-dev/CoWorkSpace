from django.db import models
from django.contrib.auth.models import AbstractUser


# Modelo personalizado de usuario
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username