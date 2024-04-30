from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("all/", views.ListAllPropertiesAPIView.as_view(), name="all-properties"),
    path(
        "myporp/", views.ListAgentsPropertiesAPIView.as_view(), name="agent-properties"
    ),
    path("create/", views.create_property_api_view, name="property-create"),
    path("createprop/", views.create_property_request_api_view, name="property-create"),
    path(
        "details/<slug:slug>/",
        views.PropertyDetailView.as_view(),
        name="property-details",
    ),
    path("photos/<slug:slug>/", views.get_property_photos, name="property_photos"),
    path("update/<slug:slug>/", views.update_property_api_view, name="update-property"),
    path("delete/<slug:slug>/", views.delete_property_api_view, name="delete-property"),
    path("search/", views.PropertySearchAPIView.as_view(), name="property-search"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
