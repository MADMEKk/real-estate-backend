import logging
import django_filters
from django.core.mail import send_mail
from django.db.models import query

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .exceptions import PropertyNotFound
from apps.users.models import User

from .models import Property, PropertyViews, Photo, Propertysellerinfo,SavedProperty,PropertyLike
from .pagination import PropertyPagination
from .serializers import (PropertyCreateSerializer, PropertySerializer,PropertyLikeSerializer,
                         SavedPropertySerializer, PropertyViewSerializer, UpdatePropertySerializer, UserSerializer)
from .permissions import IsAgentOrReadOnly, IsOwnerOrReadOnly, IsAdminOrAgent, IsAgent

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like_property(request, slug):
    try:
        property_instance = Property.objects.get(slug=slug)
        like, created = PropertyLike.objects.get_or_create(property=property_instance, user=request.user)

        if not created:
            # If the like already exists, remove it (unlike)
            like.delete()
            return Response({'message': 'Property unliked'}, status=status.HTTP_200_OK)
        else:
            # If the like was created, return the like information
            serializer = PropertyLikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Property.DoesNotExist:
        return Response({'message': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def property_likes(request, slug):
    try:
        property_instance = Property.objects.get(slug=slug)
        likes_count = PropertyLike.objects.filter(property=property_instance).count()
        return Response({'likes_count': likes_count}, status=status.HTTP_200_OK)
    except Property.DoesNotExist:
        return Response({'message': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_like_status(request, slug):
    try:
        property_instance = Property.objects.get(slug=slug)
        is_liked = PropertyLike.objects.filter(property=property_instance, user=request.user).exists()
        return Response({'is_liked': is_liked}, status=status.HTTP_200_OK)
    except Property.DoesNotExist:
        return Response({'message': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SavedPropertyAPIView(APIView):
    serializer_class = SavedPropertySerializer
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        saved_properties = SavedProperty.objects.filter(user=request.user)
        serializer = SavedPropertySerializer(saved_properties, many=True)
        return Response(serializer.data)

    def post(self, request, slug):
        try:
            property_instance = Property.objects.get(slug=slug)
            user = request.user
            saved_property, created = SavedProperty.objects.get_or_create(user=user, property=property_instance)
            if created:
                return Response({'message': 'Property saved successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Property is already saved'}, status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)


class PropertyFilter(django_filters.FilterSet):
    advert_type = django_filters.CharFilter(field_name="advert_type", lookup_expr="exact")
    property_type = django_filters.CharFilter(field_name="property_type", lookup_expr="exact")
    commune = django_filters.CharFilter(field_name="commune", lookup_expr='exact')
    daira = django_filters.CharFilter(field_name="daira", lookup_expr='exact')
    wilaya = django_filters.CharFilter(field_name="wilaya", lookup_expr='exact')
    street_address = django_filters.CharFilter(field_name="street_address", lookup_expr='icontains')
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")
    property_location = django_filters.NumberFilter(field_name="postal_code", lookup_expr="iexact")

    class Meta:
        model = Property
        fields = ["advert_type", "property_type", "wilaya", "daira", "commune", "street_address", "price", "postal_code"]

class ListAllPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    queryset = Property.published.all().order_by("-created_at")
    pagination_class = PropertyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ["commune__name", "daira__name", "wilaya__name", "title", "description"]

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Credentials"] = "True"
        response["Access-Control-Allow-Origin"] = "http://192.168.8.104:3000"
        return response

class ListAgentsPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ["wilaya__name", "commune__name", "daira__name"]
    ordering_fields = ["created_at"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated , IsAgent]

    def get_queryset(self):
        user = self.request.user
        if user.is_agent:
            return Property.objects.all().order_by("-created_at")
        return Property.published.all().order_by("-created_at")

class PropertyViewsAPIView(generics.ListAPIView):
    serializer_class = PropertyViewSerializer
    queryset = PropertyViews.objects.all()

@api_view(["GET"])
def get_property_photos(request, slug):
    property = get_object_or_404(Property, slug=slug, published_status=True)
    photos = Photo.objects.filter(property=property).values()
    return Response(list(photos), status=status.HTTP_200_OK)

class PropertyDetailView(APIView):
    def get(self, request, slug):
        property = get_object_or_404(Property, slug=slug, published_status=True)
        if request.user.is_authenticated and (request.user == property.user or request.user.is_agent):
            property = Property.objects.get(slug=slug)
        else:
            property = get_object_or_404(Property, slug=slug, published_status=True)

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")

        if not PropertyViews.objects.filter(property=property, ip=ip).exists():
            PropertyViews.objects.create(property=property, ip=ip)
            property.views += 1
            property.save()

        serializer = PropertySerializer(property, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrReadOnly])
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

     serializer = UpdatePropertySerializer(property, data=request.data, partial=True)
     if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_property_api_view(request):
    user = request.user
    data = request.data
    data["user"] = user.pkid
    photos = request.FILES.getlist("photos")
    del data["photos"]
    serializer = PropertyCreateSerializer(data=data)
    if serializer.is_valid():

        property_instance = serializer.save()
        property_id = property_instance.id
        upload_property_photos(property_id, photos)
        logger.info(f"Property {serializer.data.get('title')} created by {user.username}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrReadOnly,IsAdminOrAgent])
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Property
from .serializers import PropertySerializer

class PropertySearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PropertySerializer

    def post(self, request):
        queryset = Property.published.all()
        data = request.data

        advert_type = data.get("advert_type")
        if advert_type:
            queryset = queryset.filter(advert_type=advert_type)

        property_type = data.get("property_type", [])
        if property_type:
            queryset = queryset.filter(property_type__in=property_type)

        price_gt = data.get("price_gt")
        if price_gt is not None:
            queryset = queryset.filter(price__gt=price_gt)

        price_lt = data.get("price_lt")
        if price_lt is not None:
            queryset = queryset.filter(price__lt=price_lt)

        commune = data.get("commune")
        if commune:
            queryset = queryset.filter(commune=commune)

        daira = data.get("daira")
        if daira:
            queryset = queryset.filter(daira=daira)

        wilaya = data.get("wilaya")
        if wilaya:
            queryset = queryset.filter(wilaya=wilaya)

        street_address = data.get("street_address")
        if street_address:
            queryset = queryset.filter(street_address__icontains=street_address)

        postal_code = data.get("postal_code")
        if postal_code:
            queryset = queryset.filter(postal_code=postal_code)

        serializer = PropertySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
class PropertyRankAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PropertySerializer

    def get(self, request):
        queryset = Property.published.all()
        data = request.query_params

        advert_type = data.getlist("advert_type", [])
        property_type = data.getlist("property_type", [])
        pricegt = data.get("pricegt", 0)
        pricelt = data.get("pricelt", float('inf'))
        bedrooms = data.get("bedrooms", 0)
        bathrooms = data.get("bathrooms", 0)
        catch_phrase = data.get("catch_phrase", "")

        # Apply initial search criteria
        if advert_type:
            queryset = queryset.filter(advert_type__in=advert_type)
        if property_type:
            queryset = queryset.filter(property_type__in=property_type)
        if pricegt and pricelt:
            queryset = queryset.filter(price__gt=pricegt, price__lt=pricelt)
        if bedrooms:
            queryset = queryset.filter(bedrooms__gte=bedrooms)
        if bathrooms:
            queryset = queryset.filter(bathrooms__gte=bathrooms)
        if catch_phrase:
            queryset = queryset.filter(description__icontains=catch_phrase)

        # If no results, apply fallback mechanism
        fallback_attempts = 0
        max_fallback_attempts = 15  # Define how many fallback attempts to make

        while not queryset.exists() and fallback_attempts < max_fallback_attempts:
            fallback_attempts += 1

            # Gradually widen the price range
            pricegt = max(0, pricegt - (0.2 * pricegt))  # Decrease minimum price by 20%
            pricelt = pricelt + (0.2 * pricelt)  # Increase maximum price by 20%
            queryset = Property.published.all()
            if advert_type:
                queryset = queryset.filter(advert_type__in=advert_type)
            if property_type:
                queryset = queryset.filter(property_type__in=property_type)
            if pricegt and pricelt:
                queryset = queryset.filter(price__gt=pricegt, price__lt=pricelt)
            if bedrooms:
                queryset = queryset.filter(bedrooms__gte=bedrooms)
            if bathrooms:
                queryset = queryset.filter(bathrooms__gte=bathrooms)
            if catch_phrase:
                queryset = queryset.filter(description__icontains=catch_phrase)

        serializer = PropertySerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated, IsAdminOrAgent])
def toggle_publish_property(request, slug):
    property = get_object_or_404(Property, slug=slug)
    if request.user != property.user and not request.user.is_agent:
        return Response({"error": "You can't change the publish status of a property that doesn't belong to you"}, status=status.HTTP_403_FORBIDDEN)

    property.published_status = not property.published_status
    property.save()
    return Response({"success": "Publish status updated successfully"}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated, IsOwnerOrReadOnly,IsAdminOrAgent])
def replace_property_photo(request, property_slug, photo_id):
    try:
        property = Property.objects.get(slug=property_slug)
        photo = Photo.objects.get(id=photo_id, property=property)

        if 'file' in request.FILES:
            photo.image = request.FILES['file']
            photo.save()
            return Response("Photo replaced successfully", status=status.HTTP_200_OK)
        else:
            return Response("No photo provided", status=status.HTTP_400_BAD_REQUEST)
    except Property.DoesNotExist:
        return Response("Property not found", status=status.HTTP_404_NOT_FOUND)
    except Photo.DoesNotExist:
        return Response("Photo not found", status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAgent]


# for seller
@api_view(["POST"])
def create_property_request_api_view(request):
    data = request.data
    data["user"] = User.objects.get(is_agent=True)[1]
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
