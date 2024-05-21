from .models import Netbook, Escuela, Directivo, Informe
from rest_framework import serializers


class NetbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Netbook
        fields = '__all__'


class EscuelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escuela
        fields = '__all__'


class DirectivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directivo
        fields = '__all__'


class InformeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informe
        fields = '__all__'
