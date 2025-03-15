from django.urls import path
from .views import (
    SpaceAvailableListView, SpaceDetailView, SpaceDateAvailableListView, SpaceCreateView,
    ReservationListCreateView, ReservationDeleteView, 
)

urlpatterns = [

    # Urls para los espacions
    path('spaces/', SpaceAvailableListView.as_view(), name='spaces_available'), 
    path('spaces/create/', SpaceCreateView.as_view(), name='space_create'),    
    path('spaces/<int:pk>/', SpaceDetailView.as_view(), name='spaces_detail'),
    path("reservations/available/", SpaceDateAvailableListView.as_view(), name="spaces_available_date"),


    # Urls para las reservaciones    
    path('reservations/', ReservationListCreateView.as_view(), name='reservations_list_create'),
    path("reservations/<int:id>/", ReservationDeleteView.as_view(), name="reservation_delete"),

    
]