from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()

router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('all/', views.ListAllPropertiesAPIView.as_view(), name="all-properties"),
    path('myprop/', views.ListAgentsPropertiesAPIView.as_view(), name="agent-properties"),
    path('create/', views.create_property_api_view, name="property-create"),
    path('details/<slug:slug>/', views.PropertyDetailView.as_view(), name="property-details"),
    path('update/<slug:slug>/', views.update_property_api_view, name="update-property"),
    path('delete/<slug:slug>/', views.delete_property_api_view, name="delete-property"),
    path('search/', views.PropertySearchAPIView.as_view(), name="property-search"),
    path('rank/', views.PropertyRankAPIView.as_view(), name="property-rank"),
    path('toggle-publish/<slug:slug>/', views.toggle_publish_property, name="toggle-publish-property"),
    path('update/<slug:property_slug>/photo/<int:photo_id>/', views.replace_property_photo, name='replace-property-photo'),
    path('photos/<slug:slug>/', views.get_property_photos, name="property_photos"),
    path('saved-properties/', views.SavedPropertyAPIView.as_view(), name='saved-properties-list'),
    path('save-property/<slug:slug>/', views.SavedPropertyAPIView.as_view(), name='save-property'),
    path('toggle-like/<slug:slug>/', views.toggle_like_property, name='toggle-like-property'),
                path('likes/<slug:slug>/', views.property_likes, name='property_likes'),
            path('likestatus/<slug:slug>/', views.check_like_status, name='check-like-status'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

