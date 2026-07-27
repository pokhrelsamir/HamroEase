from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.booking_list,
        name="booking_list",
    ),

    path(
        "add/",
        views.booking_create,
        name="booking_create",
    ),

    path(
        "<int:pk>/",
        views.booking_detail,
        name="booking_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.booking_update,
        name="booking_update",
    ),

    path(
        "<int:pk>/delete/",
        views.booking_delete,
        name="booking_delete",
    ),

    # -------------------------
    # AJAX
    # -------------------------

    path(
        "api/available-rooms/",
        views.available_rooms,
        name="available_rooms",
    ),
]