from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from apps.properties.models import Property
from apps.common.models import TimeStampedUUIDModel


class Agentcontact(TimeStampedUUIDModel):
    name = models.CharField(_("Your Name"), max_length=100)
    phone_number = PhoneNumberField(
        _("Phone number"), max_length=30, default="+123456789"
    )

    email = models.EmailField(_("Email"))
    property=models.ForeignKey(Property, on_delete=models.CASCADE)
    message = models.TextField(_("Message"))

    def __str__(self):
        return self.email