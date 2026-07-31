from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Booking
from .serializers import BookingSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Bookings"],
        summary="List Bookings",
    ),
    retrieve=extend_schema(
        tags=["Bookings"],
        summary="Booking Details",
    ),
    create=extend_schema(
        tags=["Bookings"],
        summary="Create Booking",
    ),
    update=extend_schema(
        tags=["Bookings"],
        summary="Update Booking",
    ),
    partial_update=extend_schema(
        tags=["Bookings"],
        summary="Partial Update Booking",
    ),
    destroy=extend_schema(
        tags=["Bookings"],
        summary="Delete Booking",
    ),
)
class BookingViewSet(viewsets.ModelViewSet):

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)