from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.bookings.models import Booking
from apps.payments.models import Payment
from apps.reviews.models import Review

from .models import Notification


# ======================================================
# Booking Notifications
# ======================================================

@receiver(post_save, sender=Booking)
def booking_notification(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            user=instance.user,
            title="Booking Created",
            message=(
                f"Your booking for "
                f"{instance.room.hotel.name} "
                f"has been created successfully."
            ),
        )

    elif instance.status == "confirmed":

        Notification.objects.create(
            user=instance.user,
            title="Booking Confirmed",
            message=(
                f"Your booking for "
                f"{instance.room.hotel.name} "
                f"has been confirmed."
            ),
        )

    elif instance.status == "cancelled":

        Notification.objects.create(
            user=instance.user,
            title="Booking Cancelled",
            message=(
                f"Your booking for "
                f"{instance.room.hotel.name} "
                f"has been cancelled."
            ),
        )


# ======================================================
# Payment Notifications
# ======================================================

@receiver(post_save, sender=Payment)
def payment_notification(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.status == "completed":

        Notification.objects.create(
            user=instance.booking.user,
            title="Payment Successful",
            message=(
                f"Payment for "
                f"{instance.booking.room.hotel.name} "
                f"was successful."
            ),
        )

    elif instance.status == "failed":

        Notification.objects.create(
            user=instance.booking.user,
            title="Payment Failed",
            message=(
                f"Payment for "
                f"{instance.booking.room.hotel.name} "
                f"has failed."
            ),
        )


# ======================================================
# Review Notifications
# ======================================================

@receiver(post_save, sender=Review)
def review_notification(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            user=instance.user,
            title="Review Submitted",
            message=(
                f"Thank you for reviewing "
                f"{instance.hotel.name}."
            ),
        )