from django.urls import path

from . import views

urlpatterns = [

    # ======================================================
    # Hotel URLs
    # ======================================================

    path(
        "",
        views.hotel_list,
        name="hotel_list",
    ),

    path(
        "add/",
        views.hotel_create,
        name="hotel_create",
    ),

    path(
        "<int:pk>/",
        views.hotel_detail,
        name="hotel_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.hotel_update,
        name="hotel_update",
    ),

    path(
        "<int:pk>/delete/",
        views.hotel_delete,
        name="hotel_delete",
    ),

    # ======================================================
    # Room URLs
    # ======================================================

    path(
        "rooms/",
        views.room_list,
        name="room_list",
    ),

    path(
        "rooms/add/",
        views.room_create,
        name="room_create",
    ),

    path(
        "rooms/<int:pk>/",
        views.room_detail,
        name="room_detail",
    ),

    path(
        "rooms/<int:pk>/edit/",
        views.room_update,
        name="room_update",
    ),

    path(
        "rooms/<int:pk>/delete/",
        views.room_delete,
        name="room_delete",
    ),
]