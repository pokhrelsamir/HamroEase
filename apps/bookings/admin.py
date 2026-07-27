from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "booking_number",
        "guest",
        "hotel",
        "room",
        "check_in",
        "check_out",
        "status",
        "payment_status",
    )

    list_filter = (
        "status",
        "payment_status",
        "hotel",
    )

    search_fields = (
        "booking_number",
        "guest__email",
        "hotel__name",
    )