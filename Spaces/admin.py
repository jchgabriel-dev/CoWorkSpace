from django.contrib import admin
from .models import Space, Reservation

# Administracion para modelos
admin.site.register(Space)
admin.site.register(Reservation)