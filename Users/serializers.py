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
    username = serializers.CharField(
        required=True, 
        error_messages={"blank": "Este campo es obligatorio.", "required": "Este campo es obligatorio."}
    )
    password = serializers.CharField(
        required=True, 
        write_only=True,
        error_messages={"blank": "Este campo es obligatorio.", "required": "Este campo es obligatorio."}
    )
    email = serializers.EmailField(
        required=True, 
        error_messages={"blank": "Este campo es obligatorio.", "required": "Este campo es obligatorio."}
    )
      
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    

    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value



# Serializer para inicio de sesion
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    