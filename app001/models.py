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


class Cliente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    observaciones=models.TextField(blank=True)

    class Meta:
            verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"