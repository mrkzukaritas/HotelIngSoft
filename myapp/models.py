from django.db import models , transaction
from django.core.validators import MinValueValidator 
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
class TiposServicios(models.IntegerChoices):
    HABITACION = 1, 'HABITACION'
    SALON = 2, 'SALON'



class Servicio(models.Model):
    #El tipo de habitacion 
    tipo = models.IntegerField(choices=TiposServicios.choices,default=TiposServicios.HABITACION)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    personas = models.IntegerField(validators=[MinValueValidator(1)])
    especificacion = models.TextField(max_length=200)
    numero = models.IntegerField()
    disponible = models.BooleanField(default= True)

    def __str__(self):
        return str(self.numero )+ "_" +str(TiposServicios(self.tipo).label)



class Reserva(models.Model):
    nombre= models.CharField(max_length=30)
    paga = models.BooleanField(default=False)
    identificacion= models.IntegerField()
    codigo_reserva = models.CharField(max_length=20, unique=True, blank=True, default="RES")
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    servicio= models.ForeignKey(Servicio, on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return self.codigo_reserva
    
    def pagar(self):
        self.paga = True

    #hace el codigo de reserva
    def save(self, *args, **kwargs):
        if self.codigo_reserva:
            # 1. Obtener las primeras 3 letras del primer nombre en minúsculas
            
            primer_nombre = self.nombre.split()[0]
            iniciales = primer_nombre[:3].lower().capitalize()  # "Mar" para Maria
            
            # 2. Tomar los últimos 3 dígitos de la cédula
            id_str = str(self.identificacion) if self.identificacion else '000'
            ultimos_cc = id_str[-3:]  # Ahora funciona con números
            
            # 4. Generar el código con el formato solicitado
            self.codigo_reserva = f"RES-{iniciales}-{ultimos_cc}"
            
            # Guardamos nuevamente con el código generado
        with transaction.atomic():
            # Guardamos primero la reserva para obtener su ID
            super().save(*args, **kwargs)
            
            # Si tiene un servicio asociado, marcarlo como no disponible
            if self.servicio:
                Servicio.objects.filter(id=self.servicio.id).update(disponible=False)

    
@receiver(post_delete, sender= Reserva)
def liberar_servicio(sender, instance, **kwargs):
    if instance.servicio:
        Servicio.objects.filter(id=instance.servicio.id).update(disponible=True)






