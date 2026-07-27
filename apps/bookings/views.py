from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import BookingForm
from .models import Booking

from django.http import JsonResponse
from django.db.models import Q

from apps.hotels.models import Room


# =====================================================
# Booking List
# =====================================================

@login_required
def booking_list(request):

    if request.user.role == "hotel_manager":

        bookings = Booking.objects.filter(
            hotel__manager=request.user
        ).select_related(
            "guest",
            "hotel",
            "room",
        )

    else:

        bookings = Booking.objects.filter(
            guest=request.user
        ).select_related(
            "hotel",
            "room",
        )

    return render(
        request,
        "bookings/booking_list.html",
        {
            "bookings": bookings,
        },
    )


# =====================================================
# Booking Detail
# =====================================================

@login_required
def booking_detail(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
    )

    return render(
        request,
        "bookings/booking_detail.html",
        {
            "booking": booking,
        },
    )


# =====================================================
# Create Booking
# =====================================================

@login_required
def booking_create(request):

    if request.method == "POST":

        form = BookingForm(
            request.POST,
        )

        if form.is_valid():

            booking = form.save(commit=False)

            booking.guest = request.user

            nights = (
                booking.check_out -
                booking.check_in
            ).days

            booking.total_amount = (
                Decimal(nights) *
                booking.room.price_per_night
            )

            booking.save()

            messages.success(
                request,
                "Booking created successfully."
            )

            return redirect(
                "booking_detail",
                booking.pk,
            )

    else:

        form = BookingForm()

    return render(
        request,
        "bookings/booking_form.html",
        {
            "form": form,
            "title": "Book Room",
        },
    )


# =====================================================
# Update Booking
# =====================================================

@login_required
def booking_update(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        guest=request.user,
    )

    if request.method == "POST":

        form = BookingForm(
            request.POST,
            instance=booking,
        )

        if form.is_valid():

            booking = form.save(commit=False)

            nights = (
                booking.check_out -
                booking.check_in
            ).days

            booking.total_amount = (
                Decimal(nights) *
                booking.room.price_per_night
            )

            booking.save()

            messages.success(
                request,
                "Booking updated successfully."
            )

            return redirect(
                "booking_detail",
                booking.pk,
            )

    else:

        form = BookingForm(
            instance=booking,
        )

    return render(
        request,
        "bookings/booking_form.html",
        {
            "form": form,
            "title": "Edit Booking",
        },
    )


# =====================================================
# Delete Booking
# =====================================================

@login_required
def booking_delete(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        guest=request.user,
    )

    if request.method == "POST":

        booking.delete()

        messages.success(
            request,
            "Booking cancelled successfully."
        )

        return redirect(
            "booking_list"
        )

    return render(
        request,
        "bookings/booking_confirm_delete.html",
        {
            "booking": booking,
        },
    )


@login_required
def available_rooms(request):

    hotel_id = request.GET.get("hotel")
    check_in = request.GET.get("check_in")
    check_out = request.GET.get("check_out")

    if not hotel_id or not check_in or not check_out:

        return JsonResponse(
            [],
            safe=False,
        )

    booked_rooms = Booking.objects.filter(

        Q(check_in__lt=check_out) &
        Q(check_out__gt=check_in)

    ).exclude(
        status="cancelled"
    ).values_list(
        "room_id",
        flat=True,
    )

    rooms = Room.objects.filter(
        hotel_id=hotel_id,
        status="available",
    ).exclude(
        id__in=booked_rooms,
    )

    data = [

        {
            "id": room.id,
            "text": f"{room.room_number} - {room.room_type.title()}",
        }

        for room in rooms

    ]

    return JsonResponse(
        data,
        safe=False,
    )