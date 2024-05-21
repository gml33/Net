from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    detalle = models.TextField(max_length=500, blank=True)
    email = models.EmailField(max_length=30, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_incorporacion= models.DateField(null=True, blank=True)
    rol_choices = (
        ('Administrador', 'Administrador'),
        ('Rte', 'Rte'),
        ('Pedagogico', 'Pedagogico')
    )
    rol = models.CharField(max_length=100, choices=rol_choices)
    foto = models.ImageField(upload_to='profiles', blank=True)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.rol} - {self.user.first_name} {self.user.last_name}"
    
class Directivo(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    observaciones=models.TextField(blank=True)

    class Meta:
            verbose_name_plural = 'Directivos'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"    

class Escuela(models.Model):
    nombre = models.CharField(max_length=200, blank=True)
    cue = models.IntegerField(blank=True, null=True)
    cuise = models.IntegerField()
    direccion = models.CharField(max_length=200, blank=True)
    localidad = models.CharField(max_length=200, blank=True)
    departamento = models.CharField(max_length=200, blank=True)
    responsable = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, blank=True, null=True)
    directivo = models.ForeignKey(Directivo, on_delete=models.DO_NOTHING, blank=True, null=True)
    detalle = models.TextField(blank=True, null=True)

    class Meta:
            verbose_name_plural = 'Escuelas'
            ordering = ["-cuise"]

    def __str__(self):
        return f"{self.cuise} - {self.nombre}"

class Netbook(models.Model):
    identificador = models.IntegerField()
    serie = models.CharField(max_length=50, blank=True)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, blank=True)
    marca = models.CharField(max_length=50, blank=True)
    modelo = models.CharField(max_length=50, blank=True)
    imagen_win = models.CharField(max_length=50, blank=True, default='original')    
    estado_pila_choices = (
        ('Cargada', 'Cargada'),
        ('pendiente_de_cambio', 'Pendiente de Cambio'),
        ('Cambiada', 'Cambiada')
    )
    estado_pila = models.CharField(max_length=20, choices=estado_pila_choices, default='Cargada')
    arranques = models.IntegerField(blank=True, default=0)
    fecha_expiracion = models.DateField(blank=True, null=True)
    sn = models.CharField(max_length=30, blank=True)
    hid = models.CharField(max_length=20, blank=True)
    boottick = models.CharField(max_length=10, blank=True)
    estado_disco_choices = (
        ('flasheado', 'flasheado'),
        ('sin flashear', 'sin flashear')
    )
    estado_disco = models.CharField(max_length=20, choices=estado_disco_choices, default='sin flashear')
    Estado_CHOICES = (
        ('ok', 'ok'),
        ('Prestamo', 'Préstamo a docente'),
        ('no funciona', 'no funciona'),
        ('bloqueada', 'bloqueada'),
        ('pendiente de revision', 'pendiente de revision'),
        ('pendiente migracion', 'pendiente migracion'),
        ('robada', 'robada')
    )
    estado = models.CharField(max_length=30, choices=Estado_CHOICES, default="pendiente de revision")
    detalle = models.TextField(blank=True)
    
    imagen1 = models.ImageField(upload_to='netbooks', blank=True)

    class Meta:
            verbose_name_plural = 'Netbooks'

    def __str__(self):
        return f"{self.marca} - {self.serie}"


class Actividad(models.Model):
    fecha = models.DateTimeField()
    autor = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    tipo_actividad_choices = (
        ('Alta', 'Alta'),
        ('consulta', 'consulta'),
        ('modificacion', 'modificacion'),
        ('Baja', 'Baja')
    )
    tipo_actividad = models.CharField(
        max_length=20, choices=tipo_actividad_choices)
    entidad = models.CharField(max_length=100, blank=True)

    class Meta:
            verbose_name_plural = 'Actividades'

    def __str__(self):
        return f"{self.fecha} - {self.autor} - {self.tipo_actividad} - {self.entidad}"


class Informe(models.Model):
    fecha = models.DateTimeField()
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    detalle = models.TextField()
    autor = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)    
    estado = models.CharField(max_length=100, blank=False)
    imagen1 = models.ImageField(upload_to='informes', blank=True)
    imagen2 = models.ImageField(upload_to='informes', blank=True)
    imagen3 = models.ImageField(upload_to='informes', blank=True)

    class Meta:
            verbose_name_plural = 'Informes'

    def __str__(self):
        return f"{self.autor} - {self.fecha}"
    

