from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages

from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    total_usuarios = User.objects.all().count()
    data = {
        'total_usuarios': total_usuarios,
    }
    return render(request, 'app001/index.html', data)

#---------------clientes--------------------------------------------------
def agregar_cliente(request):
    data = {
        'form': ClienteForm()
    }
    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cliente agregada correctamente")
            return redirect(to="app001:listar_clientes")
        else:
            messages.warning(request, "No se pudo agregar el cliente")
            data["form"] = formulario
    return render(request, 'app001/cliente/agregar.html', data)


def listar_clientes(request):
    clientes = Cliente.objects.all().order_by('id')
    data = {
        'clientes': clientes
    }
    return render(request, 'app001/cliente/listar.html', data)


def detalle_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    data = {
        'cliente': cliente
    }
    return render(request, 'app001/cliente/detalle.html', data)


def modificar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    data = {
        'form': ClienteForm(instance=cliente)
    }
    if request.method == 'POST':
        formulario = ClienteForm(
            data=request.POST, instance=cliente, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cliente modificado correctamente")
            return redirect(to="app001:listar_clientes")
        else:
            messages.warning(request, "No se pudo modificar el cliente")
            data["form"] = formulario

    return render(request, 'app001/cliente/modificar.html', data)


def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.success(request, "cliente eliminado correctamente")
    return redirect(to="app001:listar_clientes")

# ------------------registro de usuarios--------------------

def registro(request):
    data = {
        'form1': CustomUserCreationForm,
        'form2':ProfileForm,
    }
    if request.method == 'POST':
        formulario1 = CustomUserCreationForm(data=request.POST)
        if formulario1.is_valid():
            formulario1.save()
            user = authenticate(
                username=formulario1.cleaned_data['username'], password=formulario1.cleaned_data['password1'])
            login(request, user)
            messages.success(request, "El registro fue exitoso")
            return redirect(to='app001:listar_clientes')
        else:
            data['form1'] = formulario1
    return render(request, 'registration/registro.html', data)