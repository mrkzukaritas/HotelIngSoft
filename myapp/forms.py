from django import forms
from .models import Reserva, Servicio, TiposServicios

class ReservaForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    identificacion = forms.IntegerField(label='Identificación')

    fechaInicio = forms.DateField(label='Fecha Inicio')

    fechaFin = forms.DateField(label='Fecha Final')
    servicio = forms.ChoiceField(
    choices=lambda: [
        (s.numero, f"{s.numero} - {TiposServicios(s.tipo).label}")
        for s in Servicio.objects.filter(disponible=True)
    ],
    label='Servicio'
)
class pagarReservaForm(forms.Form):

    paga = forms.BooleanField(label='Paga', required=False)
    identificacion = forms.IntegerField(label='IIngrese para validar la identificación')
