from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.hotels.models import Room

from .models import Booking
from .serializers import BookingSerializer
from .permissions import (
    IsBookingOwnerOrManager,
    IsHotelManager,
)


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

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ["ADMIN", "HOTEL_MANAGER"]:
            return Booking.objects.all()

        return Booking.objects.filter(user=user)

    def get_permissions(self):
        """
        Assign permissions based on action.
        """

        if self.action in ["confirm", "check_in", "check_out"]:
            permission_classes = [IsAuthenticated, IsHotelManager]

        elif self.action == "cancel":
            permission_classes = [IsAuthenticated, IsBookingOwnerOrManager]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_object(self):
        """
        Ensure guests cannot access other users' bookings.
        """

        booking = super().get_object()

        user = self.request.user

        if user.role in ["ADMIN", "HOTEL_MANAGER"]:
            return booking

        if booking.user != user:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "You do not have permission to access this booking."
            )

        return booking

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # ==========================================================
    # Confirm Booking
    # ==========================================================

    @extend_schema(
        tags=["Bookings"],
        summary="Confirm Booking",
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="confirm",
    )
    def confirm(self, request, pk=None):

        booking = self.get_object()

        if booking.status != Booking.Status.PENDING:
            return Response(
                {
                    "detail": "Only pending bookings can be confirmed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.CONFIRMED
        booking.save()

        return Response(
            {
                "detail": "Booking confirmed successfully."
            }
        )

    # ==========================================================
    # Cancel Booking
    # ==========================================================

    @extend_schema(
        tags=["Bookings"],
        summary="Cancel Booking",
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="cancel",
    )
    def cancel(self, request, pk=None):

        booking = self.get_object()

        if booking.status == Booking.Status.COMPLETED:
            return Response(
                {
                    "detail": "Completed bookings cannot be cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.CANCELLED
        booking.save()

        booking.room.status = "available"
        booking.room.save(update_fields=["status"])

        return Response(
            {
                "detail": "Booking cancelled successfully."
            }
        )

    # ==========================================================
    # Check In
    # ==========================================================

    @extend_schema(
        tags=["Bookings"],
        summary="Check In",
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="check-in",
    )
    def check_in(self, request, pk=None):

        booking = self.get_object()

        if booking.status != Booking.Status.CONFIRMED:
            return Response(
                {
                    "detail": "Booking must be confirmed first."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.CHECKED_IN
        booking.save()

        booking.room.status = "occupied"
        booking.room.save(update_fields=["status"])

        return Response(
            {
                "detail": "Guest checked in successfully."
            }
        )

    # ==========================================================
    # Check Out
    # ==========================================================

    @extend_schema(
        tags=["Bookings"],
        summary="Check Out",
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="check-out",
    )
    def check_out(self, request, pk=None):

        booking = self.get_object()

        if booking.status != Booking.Status.CHECKED_IN:
            return Response(
                {
                    "detail": "Guest must check in first."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.COMPLETED
        booking.save()

        booking.room.status = "available"
        booking.room.save(update_fields=["status"])

        return Response(
            {
                "detail": "Guest checked out successfully."
            }
        )

# from drf_spectacular.utils import (
#     extend_schema,
#     extend_schema_view,
# )

# from rest_framework import status, viewsets
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from .models import Booking
# from .serializers import BookingSerializer
# from .permissions import (
#     IsBookingOwnerOrManager,
#     IsHotelManager,
# )


# @extend_schema_view(
#     list=extend_schema(
#         tags=["Bookings"],
#         summary="List Bookings",
#     ),
#     retrieve=extend_schema(
#         tags=["Bookings"],
#         summary="Booking Details",
#     ),
#     create=extend_schema(
#         tags=["Bookings"],
#         summary="Create Booking",
#     ),
#     update=extend_schema(
#         tags=["Bookings"],
#         summary="Update Booking",
#     ),
#     partial_update=extend_schema(
#         tags=["Bookings"],
#         summary="Partial Update Booking",
#     ),
#     destroy=extend_schema(
#         tags=["Bookings"],
#         summary="Delete Booking",
#     ),
# )
# class BookingViewSet(viewsets.ModelViewSet):

#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user

#         if user.role in ["ADMIN", "HOTEL_MANAGER"]:
#             return Booking.objects.all()

#         return Booking.objects.filter(user=user)

#     def get_permissions(self):
#         """
#         Assign permissions based on action.
#         """

#         if self.action in ["confirm", "check_in", "check_out"]:
#             permission_classes = [IsAuthenticated, IsHotelManager]

#         elif self.action == "cancel":
#             permission_classes = [IsAuthenticated, IsBookingOwnerOrManager]

#         else:
#             permission_classes = [IsAuthenticated]

#         return [permission() for permission in permission_classes]

#     def get_object(self):
#         """
#         Ensure guests cannot access other users' bookings.
#         """

#         booking = super().get_object()

#         user = self.request.user

#         if user.role in ["ADMIN", "HOTEL_MANAGER"]:
#             return booking

#         if booking.user != user:
#             from rest_framework.exceptions import PermissionDenied

#             raise PermissionDenied(
#                 "You do not have permission to access this booking."
#             )

#         return booking

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     # ==========================================================
#     # Confirm Booking
#     # ==========================================================

#     @extend_schema(
#         tags=["Bookings"],
#         summary="Confirm Booking",
#     )
#     @action(
#         detail=True,
#         methods=["post"],
#         url_path="confirm",
#     )
#     def confirm(self, request, pk=None):

#         booking = self.get_object()

#         if booking.status != Booking.Status.PENDING:
#             return Response(
#                 {
#                     "detail": "Only pending bookings can be confirmed."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         booking.status = Booking.Status.CONFIRMED
#         booking.save()

#         return Response(
#             {
#                 "detail": "Booking confirmed successfully."
#             }
#         )

#     # ==========================================================
#     # Cancel Booking
#     # ==========================================================

#     @extend_schema(
#         tags=["Bookings"],
#         summary="Cancel Booking",
#     )
#     @action(
#         detail=True,
#         methods=["post"],
#         url_path="cancel",
#     )
#     def cancel(self, request, pk=None):

#         booking = self.get_object()

#         if booking.status == Booking.Status.COMPLETED:
#             return Response(
#                 {
#                     "detail": "Completed bookings cannot be cancelled."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         booking.status = Booking.Status.CANCELLED
#         booking.save()

#         return Response(
#             {
#                 "detail": "Booking cancelled successfully."
#             }
#         )

#     # ==========================================================
#     # Check In
#     # ==========================================================

#     @extend_schema(
#         tags=["Bookings"],
#         summary="Check In",
#     )
#     @action(
#         detail=True,
#         methods=["post"],
#         url_path="check-in",
#     )
#     def check_in(self, request, pk=None):

#         booking = self.get_object()

#         if booking.status != Booking.Status.CONFIRMED:
#             return Response(
#                 {
#                     "detail": "Booking must be confirmed first."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         booking.status = Booking.Status.CHECKED_IN
#         booking.save()

#         return Response(
#             {
#                 "detail": "Guest checked in successfully."
#             }
#         )

#     # ==========================================================
#     # Check Out
#     # ==========================================================

#     @extend_schema(
#         tags=["Bookings"],
#         summary="Check Out",
#     )
#     @action(
#         detail=True,
#         methods=["post"],
#         url_path="check-out",
#     )
#     def check_out(self, request, pk=None):

#         booking = self.get_object()

#         if booking.status != Booking.Status.CHECKED_IN:
#             return Response(
#                 {
#                     "detail": "Guest must check in first."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         booking.status = Booking.Status.COMPLETED
#         booking.save()

#         return Response(
#             {
#                 "detail": "Guest checked out successfully."
#             }
#         )