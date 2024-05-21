from django import forms
from .models import Netbook, Escuela, Informe, Actividad, Directivo, Profile
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class DirectivoForm(forms.ModelForm):

    class Meta:
        model = Directivo
        fields = ['nombres','apellidos','telefono','email']


class NetbookForm(forms.ModelForm):
    estado_pila_choices = (
        ('Cargada', 'Cargada'),
        ('pendiente_de_cambio', 'Pendiente de Cambio'),
        ('Cambiada', 'Cambiada')
    )
    estado_pila = forms.ChoiceField(
        choices=estado_pila_choices, widget=forms.RadioSelect())
    fecha_expiracion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    estado_disco_choices = (
        ('flasheado', 'flasheado'),
        ('sin flashear', 'sin flashear')
    )
    estado_disco = forms.ChoiceField(
        choices=estado_disco_choices, widget=forms.RadioSelect())

    Estado_CHOICES = (
        ('ok', 'ok'),
        ('Prestamo', 'Préstamo a docente'),
        ('no funciona', 'no funciona'),
        ('bloqueada', 'bloqueada'),
        ('pendiente de revision', 'pendiente de revision'),
        ('pendiente migracion', 'pendiente migracion'),
        ('robada', 'robada')
    )
    estado = forms.ChoiceField(choices=Estado_CHOICES,
                               widget=forms.RadioSelect())

    class Meta:
        model = Netbook
        fields = ['identificador','serie','marca','modelo','imagen_win','escuela','estado_pila',
                  'arranques','fecha_expiracion','estado_disco','estado','detalle','imagen1']


class EscuelaForm(forms.ModelForm):

    class Meta:
        model = Escuela
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('detalle', 'foto')


class InformeForm(forms.ModelForm):

    class Meta:
        model = Informe
        fields = '__all__'
        exclude = ('autor', 'fecha', 'estado')


class ActividadForm(forms.ModelForm):

    class Meta:
        model = Actividad
        fields = '__all__'
