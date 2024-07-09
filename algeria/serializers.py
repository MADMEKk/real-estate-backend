from rest_framework import serializers
from .models import Wilaya, Daira, Commune

class WilayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilaya
        fields = ['id', 'code', 'name_ascii', 'name']

class DairaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Daira
        fields = ['id', 'name_ascii', 'name', 'wilaya']

class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = ['id', 'name_ascii', 'name', 'daira']
