from django.contrib import admin
from .models import Netbook, Escuela, Informe, Actividad, Directivo, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display=["user", "detalle", "email", "fecha_nacimiento", "fecha_incorporacion", "rol", "foto"]
    list_editable=["detalle", "email", "fecha_nacimiento", "fecha_incorporacion", "rol", "foto"]
    search_fields =["rol"]
    list_filter=["rol"]
    list_per_page=30

class NetbookAdmin(admin.ModelAdmin):
    list_display = ["escuela", "identificador", "serie", "estado"]
    list_editable = ["estado"]
    search_fields = ["estado"]
    list_filter = ["estado", "escuela"]
    list_per_page = 30

class EscuelaAdmin(admin.ModelAdmin):
    list_display = ["id","cuise", "cue", "nombre", "localidad", "direccion"]
    list_editable = ["direccion", "cue", "nombre"]
    search_fields = ["localidad",  "cue", "cuise"]
    list_filter = ["localidad"]
    list_per_page = 10


class InformeAdmin(admin.ModelAdmin):
    list_display = ["fecha", "autor", "escuela"]
    search_fields = ["fecha", "autor", "escuela"]
    list_filter = ["fecha", "autor", "escuela"]
    list_per_page = 10


class ActividadAdmin(admin.ModelAdmin):
    list_display = ["fecha", "autor", "tipo_actividad", "entidad"]
    search_fields = ["fecha", "autor"]
    list_filter = ["fecha", "autor"]
    list_per_page = 50


class DirectivoAdmin(admin.ModelAdmin):
    list_display = ["nombres", "apellidos", "telefono", "email"]
    search_fields = ["apellidos" "telefono", "email"]
    list_filter = ["apellidos", "email"]
    list_per_page = 50

    # Register your models here.
admin.site.register(Netbook, NetbookAdmin)
admin.site.register(Escuela, EscuelaAdmin)
admin.site.register(Informe, InformeAdmin)
admin.site.register(Actividad, ActividadAdmin)
admin.site.register(Directivo, DirectivoAdmin)
admin.site.register(Profile, ProfileAdmin)
