from django.shortcuts import render
from django.http import HttpResponse
from .models import Servicio,Reserva
from django.shortcuts import get_object_or_404 , render, redirect
from .forms import ReservaForm

# Create your views here.

#render para redirigir a un archivo html 
# http reponse para mostrar un mensaje nomas 

def servicios_disponibles(request):
    
    servicios = Servicio.objects.all()

    return render(request,'servicios_disponibles.html',{
        'servicios': servicios,
    })

def listaReservas(request):

    reservas = Reserva.objects.all()

    return render(request,'listas_reservas.html',{

        'reservas': reservas

    })

def Reservar(request):

    if request.method == 'GET':
            return render(request,'reservar.html',
                {
        'form': ReservaForm
    })
    else:

        Reserva.objects.create(
            nombre = request.POST['nombre'],
            fechaInicio = request.POST['fechaInicio'],
            fechaFin = request.POST['fechaFin'],
            identificacion = request.POST['identificacion'],
            servicio = get_object_or_404(Servicio,numero=request.POST['servicio'])
        )
        return redirect('/listas_reservas')

#pagina principal
def index(request):
    return render(request,'index.html')

def pagarReserva(request,codigo_reserva):
    reserva = get_object_or_404(Reserva, codigo_reserva=codigo_reserva)
    reserva.pagar()
    return render(request, 'pagarReserva.html', {
        'reserva': reserva,
    })
    
    
