from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from apps.hotels.models import Hotel, Room


class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CHECKED_IN = "CHECKED_IN", "Checked In"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    check_in = models.DateField()

    check_out = models.DateField()

    guests = models.PositiveIntegerField()

    special_request = models.TextField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    total_nights = models.PositiveIntegerField(
        default=0,
        editable=False,
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError(
                "Check-out date must be after check-in."
            )

        if self.guests > self.room.max_guests:
            raise ValidationError(
                f"This room accommodates only {self.room.max_guests} guests."
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        self.total_nights = (
            self.check_out - self.check_in
        ).days

        self.total_price = (
            self.room.price_per_night * self.total_nights
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.hotel.name} - "
            f"{self.room.room_number}"
        )