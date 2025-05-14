from django import forms
from .models import Reserva, Servicio, TiposServicios
class ReservaForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    identificacion = forms.IntegerField(label='Identificación')
    fechaInicio = forms.DateField(
        label='Fecha Inicio',
        widget=forms.DateInput(attrs={'type': 'date'})  # Input tipo date de HTML5
    )
    
    fechaFin = forms.DateField(
        label='Fecha Final',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    #fechaInicio = forms.DateField(label='Fecha Inicio')
    #fechaFin = forms.DateField(label='Fecha Final')
    
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.filter(disponible=True),
        label='Servicio',
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='numero',  # Usamos el campo 'numero' como valor
        empty_label="Seleccione un servicio"
    )