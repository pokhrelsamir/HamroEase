from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        GUEST = "GUEST", "Guest"
        HOTEL_MANAGER = "HOTEL_MANAGER", "Hotel Manager"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(
        unique=True
    )

    full_name = models.CharField(
        max_length=150
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.GUEST
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    date_joined = models.DateTimeField(
        default=timezone.now
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email