from django.urls import path
from . import views


urlpatterns = [
    #ervicios_disponibles
    path('servicios_disponibles/', views.servicios_disponibles,name='servicios_disponibles'),
    #listas_reservas
    path('listas_reservas/', views.listaReservas,name='listas_reservas'),
    #reservar
    path('reservar/', views.Reservar,name='reservar'),

    path('pagarReserva/<str:codigo_reserva>/', views.pagarReserva,name='pagarReserva'),
    #pagina principal

    path('', views.index),
]