from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20, required=False)
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("user",)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})

        instance.about_me = profile_data.get("about_me", instance.about_me)
        instance.phone_number = profile_data.get("phone_number", instance.phone_number)
        # Ensure to save instance to persist changes
        instance.save()
        return instance
