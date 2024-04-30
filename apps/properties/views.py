import logging

import django_filters
from django.core.mail import send_mail
from django.db.models import query
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from rest_framework_simplejwt.authentication import JWTAuthentication
from .exceptions import PropertyNotFound
from .models import Property, PropertyViews, Photo, Propertysellerinfo
from .pagination import PropertyPagination
from .serializers import (PropertyCreateSerializer, PropertySerializer,
                          PropertyViewSerializer)

logger = logging.getLogger(__name__)


class PropertyFilter(django_filters.FilterSet):
    advert_type = django_filters.CharFilter(
        field_name="advert_type", lookup_expr="iexact"
    )

    property_type = django_filters.CharFilter(
        field_name="property_type", lookup_expr="iexact"
    )

    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Property
        fields = ["advert_type", "property_type", "price"]


class ListAllPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by("-created_at")
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Credentials"] = "true"
        # Assuming your React app runs on `http://localhost:3000`:
        response["Access-Control-Allow-Origin"] = "http://192.168.8.104:3000"
        return response

class ListAgentsPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]
    authentication_classes = [JWTAuthentication]  # Add JWT authentication
    permission_classes = [permissions.IsAuthenticated]  # Add permission class to require authentication

    def get_queryset(self):
        user = self.request.user
        queryset = Property.objects.filter(user=user).order_by("-created_at")
        return queryset


class PropertyViewsAPIView(generics.ListAPIView):
    serializer_class = PropertyViewSerializer
    queryset = PropertyViews.objects.all()
@api_view(["GET"])
def get_property_photos(request, slug):
    property = Property.objects.get(slug=slug)
    values = []
    value = Photo.objects.filter(property=property).values()
    val = list(value)
    values += val
    return Response(values, status=status.HTTP_200_OK)
class PropertyDetailView(APIView):
    def get(self, request, slug):
        if request.user == Property.objects.get(slug=slug).user:
            property = Property.objects.get(slug=slug)
        else:
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

        serializer = PropertySerializer(property, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_property_api_view(request, slug):
    try:
        property = Property.objects.get(slug=slug)
    except Property.DoesNotExist:
        raise PropertyNotFound

    user = request.user
    if property.user != user:
        return Response(
            {"error": "You can't update or edit a property that doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "PUT":
        data = request.data
        serializer = PropertySerializer(property, data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# for agents
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_property_api_view(request):
    user = request.user
    data = request.data
    data["user"] = request.user.pkid
    serializer = PropertyCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        logger.info(
            f"property {serializer.data.get('title')} created by {user.username}"
        )
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_property_api_view(request, slug):
    try:
        property = Property.objects.get(slug=slug)
    except Property.DoesNotExist:
        raise PropertyNotFound

    user = request.user
    if property.user != user:
        return Response(
            {"error": "You can't delete a property that doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "DELETE":
        delete_operation = property.delete()
        data = {}
        if delete_operation:
            data["success"] = "Deletion was successful"
        else:
            data["failure"] = "Deletion failed"
        return Response(data=data)


class PropertySearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PropertyCreateSerializer

    def post(self, request):
        queryset = Property.published.all()
        data = self.request.data

        advert_type = data["advert_type"]
        if len(advert_type) > 0:  # If advert_type is not None and not an empty string
            queryset = queryset.filter(advert_type__in=advert_type)

        property_type = data["property_type"]
        if len(property_type) > 0:
            queryset = queryset.filter(property_type__in=property_type)

        pricegt = data["pricegt"]
        pricelt = data["pricelt"]
        if pricegt & pricelt:
            queryset = queryset.filter(price__gt=pricegt, price__lt=pricelt)

        bedrooms = data["bedrooms"]

        if bedrooms:
            queryset = queryset.filter(bedrooms__gte=bedrooms)

            bathrooms = data["bathrooms"]

        if bathrooms:
            queryset = queryset.filter(bathrooms__gte=bathrooms)

        catch_phrase = data["catch_phrase"]
        if catch_phrase:
            queryset = queryset.filter(description__icontains=catch_phrase)

        serializer = PropertySerializer(queryset, many=True)

        return Response(serializer.data)


# for seller
@api_view(["POST"])
def create_property_request_api_view(request):
    data = request.data
    data["user"] = "1"
    # get firstname lastname and email from the request
    seller_info = {
        "first_name": request.data.get("first_name"),
        "last_name": request.data.get("last_name"),
        "email": request.data.get("email"),
        "phone": request.data.get("phone"),
    }
    # delete from data seller info fields
    del data["first_name"]
    del data["last_name"]
    del data["email"]
    del data["phone"]
    photos = request.FILES.getlist("photos")
    del data["photos"]

    # Assuming user is authenticated and you want to set the user ID
    property_serializer = PropertyCreateSerializer(data=data)

    if property_serializer.is_valid():
        # Save the property
        property_instance = property_serializer.save()
        property_id = property_instance.id
        upload_property_photos(property_id, photos)
        create_property_seller_info(property_id, seller_info)
        property_instance.slug
        return Response(property_instance.slug, status=status.HTTP_201_CREATED)

    return Response(property_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def upload_property_photos(property_id, photos):
    property = Property.objects.get(id=property_id)
    for photo in photos:
        Photo.objects.create(image=photo, property=property)
    return Response("Photos uploaded successfully")


def create_property_seller_info(property_id, seller_info):
    property = Property.objects.get(id=property_id)
    Propertysellerinfo.objects.create(property=property, **seller_info)
    return Response("Seller info created successfully")
