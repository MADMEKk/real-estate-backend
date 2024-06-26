from rest_framework import serializers
import json

from .models import Property, PropertyViews, Photo
from rest_framework import serializers
from algeria.models import Wilaya, Daira, Commune
from .models import Property

class WilayaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilaya
        fields = ['id', 'name', 'name_ascii', 'code']

class DairaSerializer(serializers.ModelSerializer):
    wilaya_name = serializers.CharField(source='wilaya.name', read_only=True)

    class Meta:
        model = Daira
        fields = ['id', 'name', 'name_ascii', 'wilaya', 'wilaya_name']

class CommuneSerializer(serializers.ModelSerializer):
    daira_name = serializers.CharField(source='daira.name', read_only=True)
    wilaya_name = serializers.CharField(source='daira.wilaya.name', read_only=True)

    class Meta:
        model = Commune
        fields = ['id', 'name', 'name_ascii', 'daira', 'daira_name', 'wilaya_name']


class PropertySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    commune_name = serializers.CharField(source='commune.name', read_only=True)
    daira_name = serializers.CharField(source='daira.name', read_only=True)
    wilaya_name = serializers.CharField(source='wilaya.name', read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "user",
            "profile_photo",
            "title",
            "slug",
            "ref_code",
            "description",
            "wilaya",
            "commune",
            "daira",
            "commune_name",
            "daira_name",
            "wilaya_name",
            "postal_code",
            "street_address",
            "property_number",
            "price",

            "tax",
            "final_property_price",
            "plot_area",
            "total_floors",
            "bedrooms",
            "bathrooms",
            "advert_type",
            "property_type",
            "cover_photo",
            "video",
            "photos",
            "published_status",
            "views",
            "amenities",
            "property_status",

            "neighborhood_info",
            "legal_status",
            "payment_options",
        ]

    def get_user(self, obj):
        return obj.user.username

    def get_cover_photo(self, obj):
        return obj.cover_photo.url

    def get_profile_photo(self, obj):
        return obj.user.profile.profile_photo.url

    def get_video(self, obj):
        return obj.video.url

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['title', 'description',  'wilaya', 'commune','daira', 'postal_code', 'street_address', 'property_number', 'price', 'plot_area', 'total_floors', 'bedrooms', 'bathrooms', 'advert_type', 'property_type', 'cover_photo', 'vedio','user']



class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews
        exclude = ["updated_at", "pkid"]


from .models import Property, Photo

class UpdatePropertySerializer(serializers.ModelSerializer):
    cover_photo = serializers.ImageField(required=False)
    vedio = serializers.FileField(required=False)


    class Meta:
        model = Property
        fields = [
            "title",
            "slug",
            "ref_code",
            "description",
            "wilaya",
            "commune",
            "daira",
            "postal_code",
            "street_address",
            "property_number",
            "price",
            "tax",
            "final_property_price",
            "plot_area",
            "total_floors",
            "bedrooms",
            "bathrooms",
            "advert_type",
            "property_type",
            "cover_photo",
            "vedio",
            "published_status",
            "views",
        ]

    def update(self, instance, validated_data):
        cover_photo = validated_data.pop('cover_photo', None)
        vedio = validated_data.pop('vedio', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cover_photo is not None:
            instance.cover_photo = cover_photo
        else:
            instance.cover_photo = Property.objects.get(slug=instance.slug).cover_photo

        if vedio is not None:
            instance.vedio = vedio
        else:
            instance.vedio = Property.objects.get(slug=instance.slug).vedio

        instance.save()
        return instance

# myapp/serializers.py
from .models import Property, Photo, PropertyViews, Propertysellerinfo,SavedProperty,PropertyLike
from django.contrib.auth import get_user_model

User = get_user_model()


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class PropertyViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews
        fields = '__all__'

class PropertysellerinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propertysellerinfo
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_agent']

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class UpdatePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews
        fields = '__all__'



class SavedPropertySerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title')
    property_description = serializers.CharField(source='property.description')
    property_wilaya = serializers.CharField(source='property.wilaya')
    cover_photo = serializers.CharField(source='property.cover_photo.url')
    advert_type = serializers.CharField(source='property.advert_type')
    property_type = serializers.CharField(source='property.property_type')
    property_slug = serializers.CharField(source='property.slug')
    class Meta:
        model = SavedProperty
        fields = ['property_title', 'property_slug', 'property_description','property_wilaya','advert_type','property_type','cover_photo', 'saved_at']

class PropertyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyLike
        fields = '__all__'