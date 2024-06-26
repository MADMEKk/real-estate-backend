from django.urls import path
from .views import ProfileAPIView

urlpatterns = [
    path('', ProfileAPIView.as_view(), name='profile-list'),
    path('<int:pk>/', ProfileAPIView.as_view(), name='profile-detail'),
]
