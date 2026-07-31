from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import viewsets

from .models import Hotel, Room
from .serializers import (
    HotelSerializer,
    RoomSerializer,
)


# ==========================================================
# Hotels API
# ==========================================================

@extend_schema_view(
    list=extend_schema(
        tags=["Hotels"],
        summary="List Hotels",
    ),
    retrieve=extend_schema(
        tags=["Hotels"],
        summary="Retrieve Hotel",
    ),
    create=extend_schema(
        tags=["Hotels"],
        summary="Create Hotel",
    ),
    update=extend_schema(
        tags=["Hotels"],
        summary="Update Hotel",
    ),
    partial_update=extend_schema(
        tags=["Hotels"],
        summary="Partial Update Hotel",
    ),
    destroy=extend_schema(
        tags=["Hotels"],
        summary="Delete Hotel",
    ),
)
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


# ==========================================================
# Rooms API
# ==========================================================

@extend_schema_view(
    list=extend_schema(
        tags=["Rooms"],
        summary="List Rooms",
    ),
    retrieve=extend_schema(
        tags=["Rooms"],
        summary="Retrieve Room",
    ),
    create=extend_schema(
        tags=["Rooms"],
        summary="Create Room",
    ),
    update=extend_schema(
        tags=["Rooms"],
        summary="Update Room",
    ),
    partial_update=extend_schema(
        tags=["Rooms"],
        summary="Partial Update Room",
    ),
    destroy=extend_schema(
        tags=["Rooms"],
        summary="Delete Room",
    ),
)
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer