from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    
    # Url para registro y login
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

]