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
    numero = models.IntegerField(unique=True)
    disponible = models.BooleanField(default= True)

    def __str__(self):
        return str(self.numero )+ "_" +str(TiposServicios(self.tipo).label)
    def valor_dolares(self):
        #QUIERO formatearlo a 2 decimales
        # Cambia 4000 por la tasa de cambio actual si es necesario
        tasa_cambio = 4200
        valor_dolares = self.valor / tasa_cambio
        return "{:.2f}".format(valor_dolares)
    



class Reserva(models.Model):
    nombre= models.CharField(max_length=30)
    paga = models.BooleanField(default=False)
    identificacion= models.IntegerField(validators=[MinValueValidator(3)])
    codigo_reserva = models.CharField(max_length=20, unique=True, blank=True, default="")
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    servicio= models.ForeignKey(Servicio, on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return self.codigo_reserva
    
    def pagar(self):
        self.paga = True
        self.save()

    #hace el codigo de reserva
    def save(self, *args, **kwargs):

        if not self.codigo_reserva and self.nombre and self.identificacion:
            try:
                primer_nombre = self.nombre.split()[0]
                iniciales = primer_nombre[:3].lower().capitalize()
                id_str = str(self.identificacion)
                ultimos_cc = id_str[-3:]
                self.codigo_reserva = f"RES-{iniciales}-{ultimos_cc}"
            except (AttributeError, IndexError):
                pass

            # 4. Generar el código con el formato solicitado
            self.codigo_reserva = f"RES-{iniciales}-{ultimos_cc}"

        with transaction.atomic():
            # Guardamos primero la reserva para obtener su ID
            super().save(*args, **kwargs)
            # Si tiene un servicio asociado, marcarlo como no disponible
            if self.servicio:
                Servicio.objects.filter(id=self.servicio.id).update(disponible=False)


@receiver(post_delete, sender=Reserva)
def liberar_servicio(sender, instance, **kwargs):
    """
    Libera el servicio asociado a una reserva cuando esta es eliminada.
    Usa servicio_id para evitar la carga del objeto Servicio completo.
    """
    if instance.servicio_id:  # Usamos _id para evitar cargar el objeto
        # Verificamos primero si el servicio aún existe
        if Servicio.objects.filter(id=instance.servicio_id).exists():
            Servicio.objects.filter(id=instance.servicio_id).update(disponible=True)