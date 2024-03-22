from django.urls import path
from .views import *
app_name = 'website'
urlpatterns = [
    path('', website, name="index"),
    path('properties', properties, name="properties"),
    path('property/<slug:slug>/', propertydetails, name="propdetails"),

]
