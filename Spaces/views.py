from django.shortcuts import render
from .models import Space, Reservation
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from .serializer import SpaceSerializer, ReservationSerializer, ReservationCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from rest_framework import status
from django.utils.timezone import now
from datetime import datetime
from django.utils import timezone


# ==================================================
# ESPACIOS
# ==================================================

# Api para obtener todos los espacios disponibles
class SpaceAvailableListView(ListAPIView):
    queryset = Space.objects.filter(available=True, is_active=True) 
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated]
    

# Api para obtener un espacio específico
class SpaceDetailView(RetrieveAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated]
    
    
# Api para obtener todos los espacios disponibles dada una fecha
class SpaceDateAvailableListView(APIView):
    queryset = Space.objects.filter(available=True) 
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        date_request = request.GET.get("date")

        if not date_request:
            return Response({"message": "El parámetro 'date' es requerido."}, status=400)
        
        date_value = parse_date(date_request)
        if not date_value:
            return Response({"message": "Formato de fecha inválido."}, status=400)
        
        
        spaces_available = self.get_available_spaces(date_value)         
        spaces_serialized = SpaceSerializer(spaces_available, many=True)
                
        return Response({
            "date": date_value,
            "spaces_available": spaces_serialized.data
        }, status=status.HTTP_200_OK)
    
    
    # Metodo para filtrar los espacios disponibles con una fecha
    def get_available_spaces(self, date_value):        
        start_day = timezone.make_aware(datetime.combine(date_value, datetime.min.time()))
        end_day = timezone.make_aware(datetime.combine(date_value, datetime.max.time()))

        reserved_space_ids = Reservation.objects.filter(
            start_time__lt=end_day,
            end_time__gt=start_day    
        ).values_list('space_id', flat=True)

        return Space.objects.exclude(id__in=reserved_space_ids).filter(is_active=True)



# ==================================================
# RESERVACION
# ==================================================

# Api para crear una reservacion
class ReservationListCreateView(APIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservationCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

# Api para cancelar una reservacion
class ReservationDeleteView(APIView):
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        reservation = Reservation.objects.filter(id=id).first()       
        
        if not reservation:
            return Response({"message": "Reserva no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        if reservation.user != request.user:
            return Response({"message": "Reserva no disponible para el usuario."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not self.can_be_cancelled(reservation):
            return Response({"message": "Solo puedes cancelar reservas con más de una hora de anticipación."}, status=status.HTTP_400_BAD_REQUEST)
        
        if reservation.space:
            reservation.space.available = True
            reservation.space.save()
        
        reservation.is_active = False        
        reservation.save()
        
        return Response({"message": "Reserva cancelada exitosamente."}, status=status.HTTP_200_OK)
    
    
    # Metodo para verificar que la reservacion pueda ser cancelada con una 1 hora de
    def can_be_cancelled(self, reservation):
        if reservation.start_time is None:
            return True
        
        return (reservation.start_time - now()).total_seconds() > 3600 
    


