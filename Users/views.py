from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView


# Api de registro
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario registrado"}, status=status.HTTP_201_CREATED)        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Api de inicio de sesion
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            return Response({
               'refresh': str(refresh),
               'access': str(refresh.access_token),
               'user': serializer.data
            }, status=status.HTTP_202_ACCEPTED)
        
        return Response({"message": "Credenciales invalidas"}, status=status.HTTP_401_UNAUTHORIZED)        
            
