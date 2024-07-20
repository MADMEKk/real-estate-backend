from django.contrib import admin
from django.utils.html import format_html
from .models import Property, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ('display_thumbnail', 'image')
    readonly_fields = ('display_thumbnail', 'image')
    extra = 0

    def display_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; width: auto;" />', obj.image.url)
        return None

    display_thumbnail.short_description = 'Thumbnail'

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'advert_type', 'property_type', 'published_status', 'display_cover_thumbnail')
    list_filter = ('advert_type', 'property_type', 'published_status')
    search_fields = ('title', 'description', 'slug', 'wilaya__name', 'commune__name', 'user__username')

    fieldsets = (
        ('Property Details', {
            'fields': ('title', 'ref_code', 'description', 'user')
        }),
        ('Location', {
            'fields': ('wilaya', 'daira', 'commune', 'postal_code', 'street_address', 'property_number')
        }),
        ('Property Details 2', {
            'fields': ('price', 'tax', 'plot_area', 'total_floors', 'bedrooms', 'bathrooms', 'advert_type', 'property_type')
        }),
        ('Media', {
            'fields': ('cover_photo','display_cover_thumbnail', 'video','display_video_thumbnail')
        }),
        ('Additional Info', {
            'fields': ('amenities', 'property_status', 'neighborhood_info', 'legal_status', 'payment_options')
        }),
        ('Boolean Fields', {
            'fields': ('ascenseur', 'balcon', 'cave', 'garage', 'gardien', 'interphone', 'meuble', 'parking_exterieur', 'parking_sous_sol', 'salle_deau', 'terrasse')
        }),
        ('Status', {
            'fields': ('published_status', 'views')
        }),
    )

    readonly_fields = ('slug', 'display_cover_thumbnail', 'display_video_thumbnail')  # Add any other readonly fields as needed

    inlines = [
        PhotoInline,
    ]

    def display_cover_thumbnail(self, obj):
        if obj.cover_photo:
            return format_html('<img src="{}" style="height: 50px; width: auto;" />', obj.cover_photo.url)
        return None

    display_cover_thumbnail.short_description = 'Cover Photo'

    def display_video_thumbnail(self, obj):
        if obj.video:
            return format_html('<video controls style="height: 50px; width: auto;"><source src="{}" type="video/mp4"></video>', obj.video.url)
        return None

    display_video_thumbnail.short_description = 'Video'

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'property')
    list_filter = ('property__title',)
    search_fields = ('property__title',)
