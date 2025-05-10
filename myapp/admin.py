from django.contrib import admin

# Register your models here.
from .models import Servicio,Reserva
admin.site.register(Servicio)
admin.site.register(Reserva)