from django.db import models
from django.conf import settings

from apps.hotels.models import Hotel, Room


class Booking(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("checked_in", "Checked In"),
        ("checked_out", "Checked Out"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("refunded", "Refunded"),
    ]

    booking_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    guest = models.ForeignKey(
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

    guests = models.PositiveIntegerField(default=1)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    special_request = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.booking_number

    def save(self, *args, **kwargs):

        if not self.booking_number:
            last = Booking.objects.count() + 1
            self.booking_number = f"HB{last:06d}"

        super().save(*args, **kwargs)