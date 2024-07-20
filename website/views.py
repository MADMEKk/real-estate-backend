from django.shortcuts import render, redirect
from apps.properties.models import *
from django.http import HttpResponseRedirect,JsonResponse
from django.utils.translation import activate
from django.conf import settings
from rest_framework.decorators import  permission_classes
from django.views.decorators.cache import cache_page
import json
from django.contrib.auth.models import User

def set_language(request):
    lang_code = request.GET.get('language', None)
    next_url = request.GET.get('next', '/')
    if lang_code:
        activate(lang_code)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        return response
    return HttpResponseRedirect(next_url)

def website(request):
    properties = Property.published.all().order_by('-views')[:5]
    return render(request, 'website/index.html', {'pop_properties':properties})

def register(request):
    return render(request, 'website/register.html')



def savedproperties(request):
    return render(request, 'website/savedproperties.html')

def properties(request):
    context = {
        'Property': Property,
    }
    return render(request, 'website/listeproducts.html', context)

def sellproperty(request):
    return render(request, 'website/sellproperty.html')

def propertysaved(request):
    return render(request, 'website/propertysaved.html')


def propertydetails( request, slug):
    property = Property.published.get(slug=slug)

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    if not PropertyViews.objects.filter(property=property, ip=ip).exists():
        PropertyViews.objects.create(property=property, ip=ip)

        property.views += 1
        property.save()

    return render(request, 'website/properydetails.html',{'property':property})

def createprofile(request):
     return render(request, 'website/createprofile.html')



def activateaccount(request, uid, token):
    context = {
        'uid': uid,
        'token': token,
    }
    return render(request, 'website/activation.html', context)
"""
class activateaccount(APIView):
    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}

        url = "http://localhost:8000/api/v1/auth/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return render(request, 'website/createprofile.html')
        else:
            return render(request, 'website/login.html')
 """



def login_view(request):
    next_page = request.GET.get('next', '/')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        url = "http://127.0.0.1:8000/api/v1/auth/jwt/create/"
        response = requests.post(url, json={'email': email, 'password': password})

        if response.status_code == 200:
            tokens = response.json()
            return JsonResponse(tokens)  # Return tokens in JSON response
        else:
            error_data = response.json()
            return JsonResponse({'error': error_data}, status=response.status_code)
    return render(request, 'website/login.html', {'next': next_page})