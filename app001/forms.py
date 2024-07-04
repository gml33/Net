from django import forms
from .models import Profile, Cliente
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('detalle', 'foto')