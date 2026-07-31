from rest_framework.permissions import BasePermission


class IsBookingOwner(BasePermission):
    """
    Allows access only to the owner of the booking.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsHotelManager(BasePermission):
    """
    Allows access only to Hotel Managers and Admins.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["HOTEL_MANAGER", "ADMIN"]
        )


class IsBookingOwnerOrManager(BasePermission):
    """
    Booking owner OR Hotel Manager/Admin.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user
            or request.user.role in ["HOTEL_MANAGER", "ADMIN"]
        )