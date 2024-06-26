from django.contrib import admin

from .models import Property, PropertyViews,Photo


class PropertyAdmin(admin.ModelAdmin):
    list_display = ["title", "advert_type", "property_type","published_status","wilaya","commune","street_address"]
    list_filter = ["advert_type", "property_type","published_status","wilaya"]


admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyViews)
admin.site.register(Photo)
