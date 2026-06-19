from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('servicios/', views.service_list, name='service_list'),
    path('servicios/<int:pk>/', views.service_detail, name='service_detail'),
    path('reservar/<int:pk>/', views.booking_create, name='booking_create'),
    path('reserva/<int:pk>/confirmacion/', views.booking_confirm, name='booking_confirm'),
    path('mis-reservas/', views.my_bookings, name='my_bookings'),
    path('mis-reservas/<int:pk>/cancelar/', views.booking_cancel, name='booking_cancel'),
]
