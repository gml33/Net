from importlib.resources import path
from django.conf.urls.static import static
from operator import index
from django.conf import settings
from django.urls import path
from .views import *

app_name = 'app001'


urlpatterns = [
    path('', index, name='index'),
    path('registro/', registro, name="registro"),
    # ------------clientes----------------------
    path('agregar-cliente/', agregar_cliente, name='agregar_cliente'),
    path('detalle-cliente/<id>/', detalle_cliente, name='detalle_cliente'),
    path('listar-clientes/', listar_clientes, name='listar_clientes'),
    path('modificar-cliente/<id>/', modificar_cliente, name='modificar_cliente'),
    path('eliminar-cliente/<id>/', eliminar_cliente, name='eliminar_cliente'),
]
