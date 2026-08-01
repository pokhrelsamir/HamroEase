from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.accounts.models import CustomUser
from apps.bookings.models import Booking
from apps.hotels.models import Hotel


class Review(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="review",
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    comment = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.hotel.name} - {self.rating}/5"