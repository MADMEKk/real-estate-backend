import random
import string

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from algeria.models import *
from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class PropertyPublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(PropertyPublishedManager, self)
            .get_queryset()
            .filter(published_status=True)
        )


from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
import random
import string
from algeria.models import Commune, Daira, Wilaya

class Property(TimeStampedUUIDModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        FOR_RENT = "For Rent", _("For Rent")
        AUCTION = "Auction", _("Auction")

    class PropertyType(models.TextChoices):
        APPARTEMENT = "Appartement", _("Appartement")
        VILLA = "Villa", _("Villa")
        LOCAL = "Local", _("Local")
        TERRAIN = "Terrain", _("Terrain")
        HANGAR = "Hangar", _("Hangar")
        BUNGALOW = "Bungalow", _("Bungalow")
        USINE = "Usine", _("Usine")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(
        User,
        verbose_name=_("Agent, Seller or Buyer"),
        related_name="agent_buyer",
        on_delete=models.DO_NOTHING,
    )

    title = models.CharField(verbose_name=_("Property Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(
        verbose_name=_("Property Reference Code"),
        max_length=255,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        default="Default description...update me please....",
    )

    commune = models.ForeignKey(
        Commune,
        related_name="commune",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Property commune"),
        default="1131"
    )
    daira = models.ForeignKey(
        Daira,
        related_name="daira",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Property Daira"),
        default="374"
    )
    wilaya = models.ForeignKey(
        Wilaya,
        related_name="wilaya",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Property Wilaya"),
        default="31"
    )

    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=100, default="140"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=150, default="KG8 Avenue"
    )
    property_number = models.IntegerField(
        verbose_name=_("Property Number"),
        validators=[MinValueValidator(1)],
        default=112,
    )
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=30, decimal_places=2, default=0.0
    )

    tax = models.DecimalField(
        verbose_name=_("Property Tax"),
        max_digits=6,
        decimal_places=2,
        default=0.15,
        help_text=_("15% property tax charged"),
    )
    plot_area = models.DecimalField(
        verbose_name=_("Plot Area (m^2)"), max_digits=8, decimal_places=2, default=0.0
    )
    total_floors = models.IntegerField(verbose_name=_("Number of floors"), default=0)
    bedrooms = models.IntegerField(verbose_name=_("Bedrooms"), default=1)
    bathrooms =models.IntegerField(verbose_name=_("Bathrooms"), default=1)
    advert_type = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=50,
        choices=AdvertType.choices,
        default=AdvertType.FOR_SALE,
    )

    property_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=50,
        choices=PropertyType.choices,
        default=PropertyType.APPARTEMENT,
    )

    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"), default="/house_sample.jpg", null=True, blank=True
    )
    video = models.FileField(default="/interior_sample.jpg", null=True, blank=True)

    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)
    amenities = models.TextField(verbose_name=_("Amenities"), blank=True, null=True)
    property_status = models.CharField(
        verbose_name=_("Property Status"), max_length=50, default="New"
    )

    neighborhood_info = models.TextField(verbose_name=_("Neighborhood Information"), blank=True, null=True)
    legal_status = models.CharField(
        verbose_name=_("Legal Status"), max_length=100, default="Clear"
    )
    payment_options = models.CharField(
        verbose_name=_("Payment Options"), max_length=100, default="Cash"
    )

    objects = models.Manager()
    published = PropertyPublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Property, self).save(*args, **kwargs)

    @property
    def final_property_price(self):
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage * property_price, 2)
        price_after_tax = float(round(property_price + tax_amount, 2))
        return price_after_tax


    @property
    def final_property_price(self):
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage * property_price, 2)
        price_after_tax = float(round(property_price + tax_amount, 2))
        return price_after_tax


class Photo(models.Model):
    image = models.ImageField(upload_to='property_photos')
    property = models.ForeignKey(Property, related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url


class PropertyViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=250)
    property = models.ForeignKey(
        Property, related_name="property_views", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"Total views on - {self.property.title} is - {self.property.views} view(s)"
        )

    class Meta:
        verbose_name = "Total Views on Property"
        verbose_name_plural = "Total Property Views"


class Propertysellerinfo(TimeStampedUUIDModel):
    first_name = models.CharField(verbose_name=_("First Name"), max_length=100)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=100)
    email = models.EmailField(verbose_name=_("Email"), max_length=150)
    phone = models.CharField(verbose_name=_("Phone"), max_length=15)

    property = models.ForeignKey(
        Property, related_name="property_enquiries", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Enquiry for - {self.property.title} by {self.name}"

    class Meta:
        verbose_name = "Property seller Info"
        verbose_name_plural = "Property seller Info"


# when propertysellerinfo is created, send email to the seller
@receiver(post_save, sender=Propertysellerinfo)
def send_email_to_seller(sender, instance, created, **kwargs):

    if created:
        subject = "Property Saved Successfully"
        message = f"Hello {instance.first_name}, your property {instance.property.title} has saved   , we will get back to you soon."
        from_email = "aures@mail.com"
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)


class SavedProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f'{self.user.username} saved {self.property.title}'



class PropertyLike(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('property', 'user')