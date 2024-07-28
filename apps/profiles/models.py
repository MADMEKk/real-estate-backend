from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedUUIDModel
from algeria.models import *

User = get_user_model()


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")



class Profile(TimeStampedUUIDModel):
    firstname = models.CharField(verbose_name=_("First Name"), max_length=50 ,default="firstname")
    lastname = models.CharField(verbose_name=_("Last Name"), max_length=50 , default="lastname")
    naissance = models.DateField(verbose_name=_("Date of Birth"), null=True, blank=True)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    address=models.CharField(verbose_name=_("Address"), max_length=50 ,default="Oran")
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+1234566789"
    )
    about_me = models.TextField(
        verbose_name=_("About me"), default="say something about yourself"
    )

    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/profile_default.png"
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.MALE,
        max_length=20,
    )




    def __str__(self):
        return f"{self.user.username}'s profile"