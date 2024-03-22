from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user account manager for the UserAccount model.
    """
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    def create_user(self, email, password=None, **extra_fields):
       
        if email:
            email = self.normalize_email(email).lower()
            self.email_validator(email)
        else:
            raise ValueError(_("User must have an email address"))
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
				
        if not password:
            raise ValueError(_("Superusers must have a password"))
				
        user = self.create_user(email, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        
        user.save(using=self._db )
        return user