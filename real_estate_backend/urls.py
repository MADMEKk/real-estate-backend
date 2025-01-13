from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('', include('django.conf.urls.i18n')),  # Include the i18n URL pattern for language switching
    path("supersecret/", admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/profile/", include("apps.profiles.urls")),
    path("api/v1/properties/", include("apps.properties.urls")),
    path("api/v1/ratings/", include("apps.ratings.urls")),
    path("api/v1/enquiries/", include("apps.enquires.urls")),
    path('api/v1/algeria/', include('algeria.urls')),
]

urlpatterns += i18n_patterns(
    path('', include("website.urls")),  # Include website URLs with i18n_patterns
)

admin.site.site_header = _("Real Estate Admin")
admin.site.site_title = _("Real Estate Admin Portal")
admin.site.index_title = _("Welcome to the Real Estate Portal")

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
