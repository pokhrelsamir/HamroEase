from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Amenity,
    Hotel,
    HotelImage,
    RoomAmenity,
    Room,
    RoomImage,
)

# ======================================================
# Hotel Images Inline
# ======================================================

class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1


# ======================================================
# Room Images Inline
# ======================================================

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


# ======================================================
# Amenity Admin
# ======================================================

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ======================================================
# Room Amenity Admin
# ======================================================

@admin.register(RoomAmenity)
class RoomAmenityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ======================================================
# Hotel Admin
# ======================================================

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "thumbnail_preview",
        "name",
        "manager",
        "city",
        "country",
        "star_rating",
        "is_active",
        "average_rating",
        "total_reviews",
        "created_at",
    )

    list_filter = (
        "is_active",
        "city",
        "country",
        "star_rating",
    )

    search_fields = (
        "name",
        "city",
        "country",
        "manager__email",
    )

    filter_horizontal = (
        "amenities",
    )

    readonly_fields = (
        "thumbnail_preview",
        "created_at",
        "updated_at",
    )

    inlines = [
        HotelImageInline,
    ]

    fieldsets = (

        ("Hotel Information", {
            "fields": (
                "manager",
                "name",
                "description",
                "thumbnail",
                "thumbnail_preview",
            )
        }),

        ("Location", {
            "fields": (
                "address",
                "city",
                "country",
            )
        }),

        ("Contact", {
            "fields": (
                "email",
                "phone",
            )
        }),

        ("Hotel Details", {
            "fields": (
                "star_rating",
                "amenities",
                "check_in_time",
                "check_out_time",
                "is_active",
            )
        }),

        ("System Information", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def thumbnail_preview(self, obj):

        if obj.thumbnail:

            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;">',
                obj.thumbnail.url
            )

        return "No Image"

    thumbnail_preview.short_description = "Thumbnail"


# ======================================================
# Hotel Image Admin
# ======================================================

@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "hotel",
        "image_preview",
        "uploaded_at",
    )

    readonly_fields = (
        "image_preview",
    )

    search_fields = (
        "hotel__name",
    )

    def image_preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;">',
                obj.image.url
            )

        return "No Image"

    image_preview.short_description = "Preview"


# ======================================================
# Room Admin
# ======================================================

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "room_number",
        "hotel",
        "room_type",
        "price_per_night",
        "status",
        "main_image_preview",
    )

    list_filter = (
        "room_type",
        "status",
        "hotel",
    )

    search_fields = (
        "room_number",
        "hotel__name",
    )

    filter_horizontal = (
        "amenities",
    )

    readonly_fields = (
        "main_image_preview",
        "created_at",
        "updated_at",
    )

    inlines = [
        RoomImageInline,
    ]

    fieldsets = (

        ("Room Information", {
            "fields": (
                "hotel",
                "room_number",
                "room_type",
                "description",
            )
        }),

        ("Pricing", {
            "fields": (
                "price_per_night",
            )
        }),

        ("Capacity", {
            "fields": (
                "max_guests",
                "total_beds",
                "room_size",
            )
        }),

        ("Images", {
            "fields": (
                "main_image",
                "main_image_preview",
            )
        }),

        ("Amenities", {
            "fields": (
                "amenities",
            )
        }),

        ("Status", {
            "fields": (
                "status",
            )
        }),

        ("System", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def main_image_preview(self, obj):

        if obj.main_image:

            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;">',
                obj.main_image.url
            )

        return "No Image"

    main_image_preview.short_description = "Preview"


# ======================================================
# Room Image Admin
# ======================================================

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "room",
        "image_preview",
        "uploaded_at",
    )

    readonly_fields = (
        "image_preview",
    )

    search_fields = (
        "room__room_number",
        "room__hotel__name",
    )

    def image_preview(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;">',
                obj.image.url
            )

        return "No Image"

    image_preview.short_description = "Preview"