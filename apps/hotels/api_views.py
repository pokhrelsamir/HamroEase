from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import CustomUser
from apps.permissions.permissions import IsHotelManager

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

    queryset = (
        Hotel.objects.select_related("manager")
        .prefetch_related("amenities")
    )

    serializer_class = HotelSerializer

    # Filtering
    filterset_fields = [
        "city",
        "country",
    ]

    # Searching
    search_fields = [
        "name",
        "city",
        "country",
        "address",
    ]

    # Ordering
    ordering_fields = [
        "name",
        "created_at",
    ]

    ordering = [
        "name",
    ]

    def get_permissions(self):

        if self.action == "create":
            permission_classes = [IsHotelManager]

        elif self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [IsAuthenticated]

        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):

        serializer.save(
            manager=self.request.user,
        )

    def perform_update(self, serializer):

        hotel = self.get_object()

        if (
            self.request.user.role != CustomUser.Role.ADMIN
            and hotel.manager != self.request.user
        ):
            raise PermissionDenied(
                "You do not own this hotel."
            )

        serializer.save()

    def perform_destroy(self, instance):

        if (
            self.request.user.role != CustomUser.Role.ADMIN
            and instance.manager != self.request.user
        ):
            raise PermissionDenied(
                "You do not own this hotel."
            )

        instance.delete()


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

    queryset = (
        Room.objects.select_related(
            "hotel",
            "hotel__manager",
        ).prefetch_related(
            "amenities",
        )
    )

    serializer_class = RoomSerializer

    # Filtering
    filterset_fields = [
        "hotel",
        "room_type",
        "status",
    ]

    # Searching
    search_fields = [
        "room_number",
        "hotel__name",
    ]

    # Ordering
    ordering_fields = [
        "price_per_night",
        "created_at",
        "room_number",
    ]

    ordering = [
        "room_number",
    ]

    def get_permissions(self):

        if self.action == "create":
            permission_classes = [IsHotelManager]

        elif self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [IsAuthenticated]

        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):

        hotel = serializer.validated_data["hotel"]

        if (
            self.request.user.role != CustomUser.Role.ADMIN
            and hotel.manager != self.request.user
        ):
            raise PermissionDenied(
                "You can only add rooms to your own hotel."
            )

        serializer.save()

    def perform_update(self, serializer):

        room = self.get_object()

        if (
            self.request.user.role != CustomUser.Role.ADMIN
            and room.hotel.manager != self.request.user
        ):
            raise PermissionDenied(
                "You do not own this room."
            )

        serializer.save()

    def perform_destroy(self, instance):

        if (
            self.request.user.role != CustomUser.Role.ADMIN
            and instance.hotel.manager != self.request.user
        ):
            raise PermissionDenied(
                "You do not own this room."
            )

        instance.delete()