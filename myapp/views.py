from django.shortcuts import render
from django.http import HttpResponse
from .models import Servicio,Reserva
from django.shortcuts import get_object_or_404 , render

# Create your views here.

#render para redirigir a un archivo html 
# http reponse para mostrar un mensaje nomas 

def servicios_disponibles(request):

    servicios = Servicio.objects.filter(disponible=True)

    return render(request,'servicios_disponibles.html',{
        'servicios': servicios
    })

def listaReservas(request):

    reservas = Reserva.objects.all()

    return render(request,'listas_reservas.html',{

        'reservas': reservas

    })

def Reservar(request):
    return render(request,'reservar.html')

def index(request):
    return render(request,'index.html')


