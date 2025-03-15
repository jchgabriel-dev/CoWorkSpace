from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


# Serializer general para usuarios
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


# Serializer para registro de usuarios
class RegisterSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    
    
    def validate(self, data):
        errors = {}       
        if "username" not in data:
            errors["username"] = "Este campo es obligatorio."
    
        if "password" not in data:
            errors["password"] = "Este campo es obligatorio."
    
        if "email" not in data:
            errors["password"] = "Este campo es obligatorio."

        if errors:
            raise serializers.ValidationError(errors) 

        return data
    
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user



# Serializer para inicio de sesion
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    