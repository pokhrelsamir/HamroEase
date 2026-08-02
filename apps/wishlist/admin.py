from django.contrib import admin

from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "hotel",
        "created_at",
    )

    search_fields = (
        "user__email",
        "hotel__name",
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )