from django.urls import path
from .views import *

app_name = 'website'
urlpatterns = [
    path('', website, name="index"),
    path('set_language/', set_language, name='set_language'),  # Add the set_language view
    path('properties', properties, name="properties"),
    path('property/<slug:slug>/', propertydetails, name="propdetails"),
    path('sellproperty', sellproperty, name="sellproperty"),
    path('propertysaved', propertysaved, name="propertysaved"),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('savedproperties/', savedproperties, name='savedproperties'),
    path('register/', register, name='register'),
    path('activate/<str:uid>/<str:token>/', activateaccount, name='activate'),
    path('createprofile/', createprofile, name='createprofile'),
]
