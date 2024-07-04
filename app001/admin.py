from django.contrib import admin
from .models import Profile, Cliente

class ProfileAdmin(admin.ModelAdmin):
    list_display=["user", "detalle", "email", "fecha_nacimiento", "fecha_incorporacion", "rol", "foto"]
    list_editable=["detalle", "email", "fecha_nacimiento", "fecha_incorporacion", "rol", "foto"]
    search_fields =["rol"]
    list_filter=["rol"]
    list_per_page=30

class ClienteAdmin(admin.ModelAdmin):
    list_display=["nombres", "apellidos", "telefono", "email"]
    list_editable=["telefono", "email"]
    search_fields =["nombres", "apellidos"]
    list_per_page=30

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Cliente, ClienteAdmin)
