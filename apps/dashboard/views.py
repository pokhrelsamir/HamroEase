from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.accounts.models import CustomUser
from apps.hotels.models import Hotel, Room


@login_required
def dashboard(request):

    user = request.user

    # ==========================================================
    # ADMIN DASHBOARD
    # ==========================================================

    if user.role == CustomUser.Role.ADMIN:

        context = {
            "users_count": CustomUser.objects.count(),
            "hotels_count": Hotel.objects.count(),
            "rooms_count": Room.objects.count(),
            "bookings_count": 0,
            "total_revenue": 0,
        }

        return render(
            request,
            "dashboard/admin_dashboard.html",
            context,
        )

    # ==========================================================
    # HOTEL MANAGER DASHBOARD
    # ==========================================================

    if user.role == CustomUser.Role.HOTEL_MANAGER:

        hotels = Hotel.objects.filter(
            manager=user
        )

        rooms = Room.objects.filter(
            hotel__manager=user
        )

        context = {
            "hotels_count": hotels.count(),
            "rooms_count": rooms.count(),
            "bookings_count": 0,
            "total_revenue": 0,
        }

        return render(
            request,
            "dashboard/manager_dashboard.html",
            context,
        )

    # ==========================================================
    # GUEST DASHBOARD
    # ==========================================================

    context = {
        "hotels_count": Hotel.objects.filter(
            is_active=True
        ).count(),
    }

    return render(
        request,
        "dashboard/guest_dashboard.html",
        context,
    )