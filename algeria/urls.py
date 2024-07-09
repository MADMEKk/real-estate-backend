from django.urls import path
from .views import WilayaListView, DairaListView, CommuneListView

urlpatterns = [
    path('wilayas/', WilayaListView.as_view(), name='wilaya-list'),
    path('dairas/<int:wilaya_id>/', DairaListView.as_view(), name='daira-list'),
    path('communes/<int:daira_id>/', CommuneListView.as_view(), name='commune-list'),
]
