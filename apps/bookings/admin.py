from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "hotel",
        "room",
        "check_in",
        "check_out",
        "guests",
        "status",
        "total_nights",
        "total_price",
        "created_at",
    )

    list_filter = (
        "status",
        "hotel",
        "created_at",
    )

    search_fields = (
        "user__email",
        "hotel__name",
        "room__room_number",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "total_nights",
        "total_price",
        "created_at",
        "updated_at",
    )