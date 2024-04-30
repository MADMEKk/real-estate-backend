from rest_framework import serializers
import json

from .models import Property, PropertyViews, Photo


class PropertySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
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
            "city",
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
            "photos",
            "published_status",
            "views",
        ]

    def get_user(self, obj):
        return obj.user.username

    def get_cover_photo(self, obj):
        return obj.cover_photo.url



    def get_video(self, obj):
        return obj.vedio.url

    def get_profile_photo(self, obj):
        return obj.user.profile.profile_photo.url




class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['title', 'description',  'city', 'postal_code', 'street_address', 'property_number', 'price', 'plot_area', 'total_floors', 'bedrooms', 'bathrooms', 'advert_type', 'property_type', 'cover_photo', 'vedio','user']



class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews
        exclude = ["updated_at", "pkid"]




