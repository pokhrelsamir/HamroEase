from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)

from rest_framework import filters, viewsets

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
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search by hotel name, city, country or address",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="city",
                description="Filter hotels by city",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="country",
                description="Filter hotels by country",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="ordering",
                description=(
                    "Order results by: "
                    "name, -name, created_at, -created_at"
                ),
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
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

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "city",
        "country",
    ]

    search_fields = [
        "name",
        "city",
        "country",
        "address",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]


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

# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
# )

# from rest_framework import viewsets

# from .models import Hotel, Room
# from .serializers import (
#     HotelSerializer,
#     RoomSerializer,
# )


# # ==========================================================
# # Hotels API
# # ==========================================================

# @extend_schema_view(
#     list=extend_schema(
#         tags=["Hotels"],
#         summary="List Hotels",
#     ),
#     retrieve=extend_schema(
#         tags=["Hotels"],
#         summary="Retrieve Hotel",
#     ),
#     create=extend_schema(
#         tags=["Hotels"],
#         summary="Create Hotel",
#     ),
#     update=extend_schema(
#         tags=["Hotels"],
#         summary="Update Hotel",
#     ),
#     partial_update=extend_schema(
#         tags=["Hotels"],
#         summary="Partial Update Hotel",
#     ),
#     destroy=extend_schema(
#         tags=["Hotels"],
#         summary="Delete Hotel",
#     ),
# )
# class HotelViewSet(viewsets.ModelViewSet):
#     queryset = Hotel.objects.all()
#     serializer_class = HotelSerializer


# # ==========================================================
# # Rooms API
# # ==========================================================

# @extend_schema_view(
#     list=extend_schema(
#         tags=["Rooms"],
#         summary="List Rooms",
#     ),
#     retrieve=extend_schema(
#         tags=["Rooms"],
#         summary="Retrieve Room",
#     ),
#     create=extend_schema(
#         tags=["Rooms"],
#         summary="Create Room",
#     ),
#     update=extend_schema(
#         tags=["Rooms"],
#         summary="Update Room",
#     ),
#     partial_update=extend_schema(
#         tags=["Rooms"],
#         summary="Partial Update Room",
#     ),
#     destroy=extend_schema(
#         tags=["Rooms"],
#         summary="Delete Room",
#     ),
# )
# class RoomViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer