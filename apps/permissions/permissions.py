from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
        )


class IsHotelManager(BasePermission):
    """
    Allows access only to hotel managers.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "manager"
        )


class IsHotelOwnerOrReadOnly(BasePermission):
    """
    Anyone can view.
    Only the hotel's manager can modify it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.manager == request.user


class IsBookingOwner(BasePermission):
    """
    Only the booking owner can access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsReviewOwner(BasePermission):
    """
    Only the review owner can modify/delete it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class IsPaymentOwner(BasePermission):
    """
    Only the payment owner can access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.booking.user == request.user