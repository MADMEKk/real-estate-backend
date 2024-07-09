from rest_framework import generics
from .models import Wilaya, Daira, Commune
from .serializers import WilayaSerializer, DairaSerializer, CommuneSerializer

class WilayaListView(generics.ListAPIView):
    queryset = Wilaya.objects.all()
    serializer_class = WilayaSerializer

class DairaListView(generics.ListAPIView):
    serializer_class = DairaSerializer

    def get_queryset(self):
        wilaya_id = self.kwargs['wilaya_id']
        return Daira.objects.filter(wilaya_id=wilaya_id)

class CommuneListView(generics.ListAPIView):
    serializer_class = CommuneSerializer

    def get_queryset(self):
        daira_id = self.kwargs['daira_id']
        return Commune.objects.filter(daira_id=daira_id)
