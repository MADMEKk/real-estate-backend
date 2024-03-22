from django.shortcuts import render
from apps.properties.models import *

# Create your views here.


def website(request):
    properties = Property.published.all().order_by('-views')[:5]
    return render(request, 'website/index.html', {'pop_properties':properties})


def properties(request):
    return render(request, 'website/listeproducts.html')




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

