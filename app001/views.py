from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.utils import timezone, dateformat
import requests
from django.contrib.auth.models import User

from app001.forms import NetbookForm
from .models import *
from django.contrib import messages

from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def index(request):
    netbooks = Netbook.objects.all()[:5]
    escuelas = Escuela.objects.all().order_by('-cuise')[:5]
    actividades = Actividad.objects.filter(
        autor=Profile.objects.get(pk=request.user.id)).order_by('-id')[:5]
    total_netbooks = Netbook.objects.all().count()
    netbooks_pendientes_de_revision = Netbook.objects.filter(
        estado='pendiente de revision').count()
    netbooks_robadas = Netbook.objects.filter(estado='robada').count()
    total_escuelas = Escuela.objects.all().count()
    total_actividades = Actividad.objects.all().count()
    total_usuarios = User.objects.all().count()
    data = {
        'netbooks': netbooks,
        'escuelas': escuelas,
        'actividades': actividades,
        'total_netbooks': total_netbooks,
        'total_escuelas': total_escuelas,
        'total_actividades': total_actividades,
        'total_usuarios': total_usuarios,
        'netbooks_pendientes_de_revision': netbooks_pendientes_de_revision,
        'netbooks_robadas': netbooks_robadas
    }
    return render(request, 'app001/index.html', data)


@permission_required('app001.add_netbook')
def agregar_netbook(request):
    data = {
        'form': NetbookForm()
    }
    if request.method == 'POST':
        formulario = NetbookForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data_actividad = {
                'fecha': timezone.now(),
                'autor': User.objects.get(pk=request.user.id),
                'tipo_actividad': 'Alta',
                'entidad': 'Netbook id: '+str(Netbook.objects.last().pk)
            }
            formulario_actividad = ActividadForm(data_actividad)
            formulario_actividad.save()
            messages.success(request, "Netbook agregada correctamente")
            return redirect(to="app001:listar_netbooks")
        else:
            messages.warning(request, "No se pudo agregar el equipo")
            data["form"] = formulario
    return render(request, 'app001/netbook/agregar.html', data)


@permission_required('app001.view_netbook')
def listar_netbooks(request):
    netbooks = Netbook.objects.all().order_by('escuela', 'identificador')
    data_act = {
        'fecha': timezone.now(),
        'autor': Profile.objects.get(pk=request.user.id),
        'tipo_actividad': 'consulta',
        'entidad': 'Netbooks'
    }
    formulario_act = ActividadForm(data_act)
    formulario_act.save()
    data = {
        'netbooks': netbooks
    }
    return render(request, 'app001/netbook/listar.html', data)


@permission_required('app001.view_netbook')
def detalle_netbook(request, id):
    netbook = get_object_or_404(Netbook, id=id)
    data = {
        'netbook': netbook
    }
    data_act = {
        'fecha': timezone.now(),
        'autor': Profile.objects.get(pk=request.user.id),
        'tipo_actividad': 'consulta',
        'entidad': 'Netbook id:'+str(netbook.id)+''
    }
    formulario_act = ActividadForm(data_act)
    formulario_act.save()
    return render(request, 'app001/netbook/detalle.html', data)


@permission_required('app001.change_netbook')
def modificar_netbook(request, id):
    netbook = get_object_or_404(Netbook, id=id)
    data = {
        'form': NetbookForm(instance=netbook)
    }
    if request.method == 'POST':
        formulario = NetbookForm(
            data=request.POST, instance=netbook, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data_act = {
                'fecha': timezone.now(),
                'autor': Profile.objects.get(pk=request.user.id),
                'tipo_actividad': 'modificacion',
                'entidad': f'Netbook id: netbook.{id}'
            }
            formulario_act = ActividadForm(data_act)
            formulario_act.save()
            messages.success(request, "Netbook modificada correctamente")
            return redirect(to="app001:listar_netbooks")
        else:
            messages.warning(request, "No se pudo modificar el equipo")
            data["form"] = formulario

    return render(request, 'app001/netbook/modificar.html', data)


@permission_required('app001.delete_netbook')
def eliminar_netbook(request, id):
    netbook = get_object_or_404(Netbook, id=id)
    identificador = str(netbook.id)
    data_act = {
        'fecha': timezone.now(),
        'autor': Profile.objects.get(pk=request.user.id),
        'tipo_actividad': 'Baja',
        'entidad': 'Netbook id: ' + identificador
    }
    formulario_act = ActividadForm(data_act)
    formulario_act.save()
    netbook.delete()
    messages.success(request, "Netbook eliminada correctamente")
    return redirect(to="app001:listar_netbooks")


# ------------Escuelas-------------------------------------------
@permission_required('app001.add_escuela')
def agregar_escuela(request):
    data = {
        'form_escuela': EscuelaForm()
    }
    if request.method == 'POST':
        formulario_escuela = EscuelaForm(request.POST)
        if formulario_escuela.is_valid():
            formulario_escuela.save()
            data_actividad = {
                'fecha': timezone.now(),
                'autor': Profile.objects.get(pk=request.user.id),
                'tipo_actividad': 'Alta',
                'entidad': 'Escuela id: '+str(Escuela.objects.last().pk)
            }
            formulario_actividad = ActividadForm(data_actividad)
            formulario_actividad.save()
            # ---------agregar for con datos de las netbooks asociadas a la escuela
            cuise_escuela = Escuela.objects.last().cuise
            for i in range(1, 31):
                data_netbook = {
                    'identificador': int(i),
                    'serie': str(str(i)+'-'+str(cuise_escuela)),
                    'escuela': Escuela.objects.last().pk,
                    'estado_pila': 'Cargada',
                    'estado_disco': 'sin flashear',
                    'estado': 'pendiente de revision',
                    'fecha_expiracion': datetime.now()
                }
                form_netbook = NetbookForm(data_netbook)
                if form_netbook.is_valid():
                    form_netbook.save()
                    data_actividad_2 = {
                        'fecha': timezone.now(),
                        'autor': Profile.objects.get(pk=request.user.id),
                        'tipo_actividad': 'Alta',
                        'entidad': 'Netbook id: '+str(Netbook.objects.last().pk)
                    }
                    formulario_actividad_2 = ActividadForm(data_actividad_2)
                    formulario_actividad_2.save()
                else:
                    print(form_netbook.errors)
            messages.success(request, "Escuela agregada correctamente")
            return redirect(to="app001:listar_escuelas")
        else:
            data = {
        'form_escuela': EscuelaForm()
    }
    return render(request, 'app001/escuela/agregar.html', data)


@permission_required('app001.view_escuela')
def listar_escuelas(request):
    escuelas = Escuela.objects.all().order_by('cuise')
    data = {
        'escuelas': escuelas
    }
    data_act = {
        'fecha': timezone.now(),
        'autor': Profile.objects.get(pk=request.user.id),
        'tipo_actividad': 'consulta',
        'entidad': 'Escuelas'
    }
    formulario_act = ActividadForm(data_act)
    formulario_act.save()
    return render(request, 'app001/escuela/listar.html', data)


@permission_required('app001.view_escuela')
def detalle_escuela(request, id):
    escuela = get_object_or_404(Escuela, id=id)
    netbooks = Netbook.objects.filter(escuela=escuela).order_by('identificador')
    netbooks_ok = Netbook.objects.filter(escuela=escuela, estado='ok').count()
    netbooks_no_funcionan = Netbook.objects.filter(escuela=escuela, estado='no funciona').count()
    netbooks_bloqueadas = Netbook.objects.filter(escuela=escuela, estado='bloqueada').count()
    netbooks_pendientes = Netbook.objects.filter(escuela=escuela, estado='pendiente de revision').count()
    netbooks_migracion = Netbook.objects.filter(escuela=escuela, estado='pendiente migracion').count()
    robadas = Netbook.objects.filter(escuela=escuela, estado='robada').count()
    data = {
        'escuela': escuela,
        'netbooks': netbooks,
        'netbooks_ok': netbooks_ok,
        'netbooks_no_funcionan': netbooks_no_funcionan,
        'netbooks_bloqueadas': netbooks_bloqueadas,
        'netbooks_pendientes': netbooks_pendientes,
        'netbooks_migracion': netbooks_migracion,
        'robadas': robadas
    }
    data_act = {
        'fecha': timezone.now(),
        'autor': Profile.objects.get(pk=request.user.id),
        'tipo_actividad': 'consulta',
        'entidad': 'Escuela N° '+str(escuela.cuise)
    }
    formulario_act = ActividadForm(data_act)
    formulario_act.save()
    return render(request, 'app001/escuela/detalle.html', data)


@permission_required('app001.change_escuela')
def modificar_escuela(request, id):
    escuela = get_object_or_404(Escuela, id=id)
    data = {
        'form': EscuelaForm(instance=escuela)
    }
    if request.method == 'POST':
        formulario = EscuelaForm(data=request.POST, instance=escuela)
        if formulario.is_valid():
            formulario.save()
            data_act = {
                'fecha': timezone.now(),
                'autor': Profile.objects.get(pk=request.user.id),
                'tipo_actividad': 'modificacion',
                'entidad': 'Escuela N° '+str(escuela.cuise)
            }
            formulario_act = ActividadForm(data_act)
            formulario_act.save()
            messages.success(request, "Escuela modificada correctamente")
            return redirect(to="app001:listar_escuelas")
        else:
            data["form"] = formulario

    return render(request, 'app001/escuela/modificar.html', data)


@permission_required('app001.delete_escuela')
def eliminar_escuela(request, id):
    escuela = get_object_or_404(Escuela, id=id)
    escuela.delete()
    messages.success(request, "Escuela eliminada correctamente")
    return redirect(to="app001:listar_escuelas")

# ------------Directivos-----------------------------------


@permission_required('app001.add_directivo')
def agregar_directivo(request):
    data = {
        'form': DirectivoForm()
    }
    if request.method == 'POST':
        formulario = DirectivoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data_actividad = {
                'fecha': timezone.now(),
                'autor': Profile.objects.get(pk=request.user.id),
                'tipo_actividad': 'Alta',
                'entidad': 'Directivo id: '+str(Directivo.objects.last().pk)
            }
            formulario_actividad = ActividadForm(data_actividad)
            formulario_actividad.save()
            messages.success(request, "Directivo agregado correctamente")
            return redirect(to="app001:listar_directivos")
        else:
            data["form"] = formulario
    return render(request, 'app001/directivo/agregar.html', data)


@permission_required('app001.view_directivo')
def listar_directivos(request):
    directivos = Directivo.objects.all()
    data = {
        'directivos': directivos
    }
    data_act = {
        'fecha': timezone.now(),
        'autor': Profile.objects.get(pk=request.user.id),
        'tipo_actividad': 'consulta',
        'entidad': 'Directivos'
    }
    formulario_act = ActividadForm(data_act)
    formulario_act.save()
    return render(request, 'app001/directivo/listar.html', data)


@permission_required('app001.view_directivo')
def detalle_directivo(request, id):
    directivo = Directivo.objects.get(id=id)
    data = {
        'directivo': directivo
    }
    data_act = {
        'fecha': timezone.now(),
        'autor': Profile.objects.get(pk=request.user.id),
        'tipo_actividad': 'consulta',
        'entidad': 'Directivo id: '+str(directivo.id)
    }
    formulario_act = ActividadForm(data_act)
    formulario_act.save()
    return render(request, 'app001/directivo/detalle.html', data)


@permission_required('app001.change_directivo')
def modificar_directivo(request, id):
    directivo = get_object_or_404(Directivo, id=id)
    data = {
        'form': DirectivoForm(instance=directivo)
    }
    if request.method == 'POST':
        formulario = DirectivoForm(data=request.POST, instance=directivo)
        if formulario.is_valid():
            formulario.save()
            data_act = {
                'fecha': timezone.now(),
                'autor': Profile.objects.get(pk=request.user.id),
                'tipo_actividad': 'modificacion',
                'entidad': 'Directivo'
            }
            formulario_act = ActividadForm(data_act)
            formulario_act.save()
            messages.success(request, "Directivo modificado correctamente")
            return redirect(to="app001:listar_directivos")
        else:
            data["form"] = formulario

    return render(request, 'app001/directivo/modificar.html', data)


@permission_required('app001.delete_directivo')
def eliminar_directivo(request, id):
    directivo = get_object_or_404(Directivo, id=id)
    directivo.delete()
    messages.success(request, "Directivo eliminado correctamente")
    return redirect(to="app001:listar_directivos")

    # ------------------------informes-----------------------------------


@permission_required('app001.add_informe')
def agregar_informe(request):
    informe = []
    data = {
        'form': InformeForm()
    }
    if request.method == 'POST':
        formulario = InformeForm(data=request.POST)
        if formulario.is_valid():
            informe = formulario.save(commit=False)
            informe.autor = Profile.objects.get(pk=request.user.id)
            informe.fecha = timezone.now()
            informe.status = 'activo'
            informe.save()
            data_actividad = {
                'fecha': timezone.now(),
                'autor': Profile.objects.get(pk=request.user.id),
                'tipo_actividad': 'Alta',
                'entidad': 'Informe id: '+str(Informe.objects.last().pk)
            }
            formulario_actividad = ActividadForm(data_actividad)
            formulario_actividad.save()
            messages.success(request, "Informe agregado correctamente")
            return redirect(to="app001:listar_informes")
        else:
            data["form"] = formulario
    return render(request, 'app001/informe/agregar.html', data)


@permission_required('app001.view_informe')
def listar_informes(request):
    usuario = Profile.objects.get(pk=request.user.id)
    informes = Informe.objects.filter(autor=usuario).order_by('-fecha')
    data_act = {
        'fecha': timezone.now(),
        'autor': Profile.objects.get(pk=request.user.id),
        'tipo_actividad': 'consulta',
        'entidad': 'Informes'
    }
    formulario_act = ActividadForm(data_act)
    formulario_act.save()
    data = {
        'informes': informes
    }
    return render(request, 'app001/informe/listar.html', data)


@ permission_required('app001.view_informe')
def detalle_informe(request, id):
    informe = get_object_or_404(Informe, id=id)
    data = {
        'informe': informe,
    }
    data_act = {
        'fecha': timezone.now(),
        'autor': Profile.objects.get(pk=request.user.id),
        'tipo_actividad': 'consulta',
        'entidad': 'Informe id: '+str(informe.id)
    }
    formulario_act = ActividadForm(data_act)
    formulario_act.save()
    return render(request, 'app001/informe/detalle.html', data)


@ permission_required('app001.change_informe')
def modificar_informe(request, id):
    informe = get_object_or_404(Informe, id=id)
    data = {
        'form': InformeForm(instance=informe)
    }
    if request.method == 'POST':
        formulario = InformeForm(data=request.POST, instance=informe)
        if formulario.is_valid(commit=False):
            formulario.save()
            data_act = {
                'fecha': timezone.now(),
                'autor': Profile.objects.get(pk=request.user.id),
                'tipo_actividad': 'modificacion',
                'entidad': 'informe id: '+str(informe.id)
            }
            formulario_act = ActividadForm(data_act)
            formulario_act.save()
            messages.success(request, "Informe modificado correctamente")
            return redirect(to="app001:listar_informes")
        else:
            data["form"] = formulario

    return render(request, 'app001/informe/modificar.html', data)


@ permission_required('app001.delete_informe')
def eliminar_informe(request, id):
    informe = get_object_or_404(Informe, id=id)
    informe.delete()
    messages.success(request, "Informe eliminado correctamente")
    return redirect(to="app001:listar_informes")


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
            return redirect(to='app001:listar_escuelas')
        else:
            data['form1'] = formulario1
    return render(request, 'registration/registro.html', data)

# ------------------reportes-------------------------------


def crear_reporte(request, id):
    fecha = datetime.now()
    solicitante = Profile.objects.get(pk=request.user.id)
    escuela = Escuela.objects.get(id=id)
    netbooks = Netbook.objects.filter(
        escuela=escuela).order_by('identificador')
    netbooks_ok = Netbook.objects.filter(escuela=escuela, estado='ok').count()
    netbooks_no_funcionan = Netbook.objects.filter(
        escuela=escuela, estado='no funciona').count()
    netbooks_bloqueadas = Netbook.objects.filter(
        escuela=escuela, estado='bloqueada').count()
    netbooks_pendientes = Netbook.objects.filter(
        escuela=escuela, estado='pendiente de revision').count()
    netbooks_migracion = Netbook.objects.filter(
        escuela=escuela, estado='pendiente migracion').count()
    robadas = Netbook.objects.filter(escuela=escuela, estado='robada').count()
    informes = Informe.objects.filter(escuela=escuela)
    directivo = Directivo.objects.get(escuela=escuela)
    data = {'escuela': escuela,
            'netbooks': netbooks,
            'informes': informes,
            'directivo': directivo,
            'fecha': fecha,
            'solicitante': solicitante,
            'netbooks_ok': netbooks_ok,
            'netbooks_no_funcionan': netbooks_no_funcionan,
            'netbooks_bloqueadas': netbooks_bloqueadas,
            'netbooks_pendientes': netbooks_pendientes,
            'netbooks_migracion': netbooks_migracion,
            'robadas': robadas,
            }
    return render(request, 'app001/reporte/crear.html', data)
