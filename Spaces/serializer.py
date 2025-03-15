from rest_framework import serializers
from .models import Space, Reservation



# ==================================================
# ESPACIOS
# ==================================================

# Serializer para espacios
class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = '__all__'


class SpaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = '__all__'

    def validate(self, data):
        errors = {}
        if "name" not in data:
            errors["name"] = "Este campo es obligatorio." 

        if errors:
            raise serializers.ValidationError(errors) 

        return data

# Serializer para espacios con solo el nombre
class SpaceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ['id', 'name'] 


# ==================================================
# RESERVACION
# ==================================================

# Serializer para listar reservaciones
class ReservationSerializer(serializers.ModelSerializer):
    space = SpaceNameSerializer()
    
    class Meta:
        model = Reservation
        fields = '__all__'


# Serializer para crear reservaciones
class ReservationCreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Reservation
        fields = '__all__'
    
    
    def validate_space(self, value):
        if not Space.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("El espacio seleccionado no existe.")
        return value
    
    
    def validate(self, data):
        errors = {}

        if "space" not in data or not data["space"]:
            errors["space"] = "Este campo es obligatorio."
        if "start_time" not in data:
            errors["start_time"] = "Este campo es obligatorio."
        if "end_time" not in data:
            errors["end_time"] = "Este campo es obligatorio."

        if errors:
            raise serializers.ValidationError(errors) 

        return data