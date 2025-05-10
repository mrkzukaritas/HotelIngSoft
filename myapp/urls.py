from django.urls import path
from . import views


urlpatterns = [
    #ervicios_disponibles
    path('servicios_disponibles/', views.servicios_disponibles),
    #listas_reservas
    path('listas_reservas/', views.listaReservas),
    #reservar
    path('reservar/', views.Reservar),
    path('', views.index),
]