from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import HotelForm, RoomForm
from .models import Hotel, Room


# ======================================================
# HOTEL CRUD
# ======================================================

@login_required
def hotel_list(request):

    hotels = Hotel.objects.filter(
        manager=request.user
    )

    return render(
        request,
        "hotels/hotels/hotel_list.html",
        {
            "hotels": hotels,
        },
    )


@login_required
def hotel_detail(request, pk):

    hotel = get_object_or_404(
        Hotel,
        pk=pk,
        manager=request.user,
    )

    return render(
        request,
        "hotels/hotels/hotel_detail.html",
        {
            "hotel": hotel,
        },
    )


@login_required
def hotel_create(request):

    if request.method == "POST":

        form = HotelForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            hotel = form.save(commit=False)

            hotel.manager = request.user

            hotel.save()

            form.save_m2m()

            messages.success(
                request,
                "Hotel created successfully."
            )

            return redirect("hotel_list")

    else:

        form = HotelForm()

    return render(
        request,
        "hotels/hotels/hotel_form.html",
        {
            "form": form,
            "title": "Add Hotel",
        },
    )


@login_required
def hotel_update(request, pk):

    hotel = get_object_or_404(
        Hotel,
        pk=pk,
        manager=request.user,
    )

    if request.method == "POST":

        form = HotelForm(
            request.POST,
            request.FILES,
            instance=hotel,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Hotel updated successfully."
            )

            return redirect("hotel_list")

    else:

        form = HotelForm(instance=hotel)

    return render(
        request,
        "hotels/hotels/hotel_form.html",
        {
            "form": form,
            "title": "Edit Hotel",
        },
    )


@login_required
def hotel_delete(request, pk):

    hotel = get_object_or_404(
        Hotel,
        pk=pk,
        manager=request.user,
    )

    if request.method == "POST":

        hotel.delete()

        messages.success(
            request,
            "Hotel deleted successfully."
        )

        return redirect("hotel_list")

    return render(
        request,
        "hotels/hotels/hotel_confirm_delete.html",
        {
            "hotel": hotel,
        },
    )


# ======================================================
# ROOM CRUD
# ======================================================

@login_required
def room_list(request):

    rooms = Room.objects.filter(
        hotel__manager=request.user
    ).select_related("hotel")

    return render(
        request,
        "hotels/rooms/room_list.html",
        {
            "rooms": rooms,
        },
    )


@login_required
def room_detail(request, pk):

    room = get_object_or_404(
        Room,
        pk=pk,
        hotel__manager=request.user,
    )

    return render(
        request,
        "hotels/rooms/room_detail.html",
        {
            "room": room,
        },
    )


@login_required
def room_create(request):

    if request.method == "POST":

        form = RoomForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            room = form.save(commit=False)

            if room.hotel.manager != request.user:

                messages.error(
                    request,
                    "You cannot add a room to another manager's hotel."
                )

                return redirect("room_list")

            room.save()

            form.save_m2m()

            messages.success(
                request,
                "Room created successfully."
            )

            return redirect("room_list")

    else:

        form = RoomForm()

        form.fields["hotel"].queryset = Hotel.objects.filter(
            manager=request.user
        )

    return render(
        request,
        "hotels/rooms/room_form.html",
        {
            "form": form,
            "title": "Add Room",
        },
    )


@login_required
def room_update(request, pk):

    room = get_object_or_404(
        Room,
        pk=pk,
        hotel__manager=request.user,
    )

    if request.method == "POST":

        form = RoomForm(
            request.POST,
            request.FILES,
            instance=room,
        )

        form.fields["hotel"].queryset = Hotel.objects.filter(
            manager=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Room updated successfully."
            )

            return redirect("room_list")

    else:

        form = RoomForm(instance=room)

        form.fields["hotel"].queryset = Hotel.objects.filter(
            manager=request.user
        )

    return render(
        request,
        "hotels/rooms/room_form.html",
        {
            "form": form,
            "title": "Edit Room",
        },
    )


@login_required
def room_delete(request, pk):

    room = get_object_or_404(
        Room,
        pk=pk,
        hotel__manager=request.user,
    )

    if request.method == "POST":

        room.delete()

        messages.success(
            request,
            "Room deleted successfully."
        )

        return redirect("room_list")

    return render(
        request,
        "hotels/rooms/room_confirm_delete.html",
        {
            "room": room,
        },
    )