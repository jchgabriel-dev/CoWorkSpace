from django.db import models
from Users.models import CustomUser

# Modelo de espacioes
class Space(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)  
    available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)    

    def __str__(self):
        return self.name
    


# Modelo de reservaciones
class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)