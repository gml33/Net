from app001.models import Netbook, Escuela, Directivo
from rest_framework import viewsets, permissions
from .serializers import NetbookSerializer, EscuelaSerializer, DirectivoSerializer


class NetbookViewset(viewsets.ModelViewSet):
    queryset = Netbook.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = NetbookSerializer

    def get_queryset(self):
        netbooks = Netbook.objects.all()

        estado = self.request.GET.get('estado')

        if estado:
            netbooks = netbooks.filter(estado=estado)

        return netbooks


class EscuelaViewset(viewsets.ModelViewSet):
    queryset = Escuela.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EscuelaSerializer

    def get_queryset(self):
        escuelas = Escuela.objects.all()
        return escuelas


class DirectivoViewset(viewsets.ModelViewSet):
    queryset = Directivo.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DirectivoSerializer

    def get_queryset(self):
        directivos = Directivo.objects.all()
        return directivos
