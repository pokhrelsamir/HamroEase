from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)

from apps.accounts.models import CustomUser


# ==========================================================
# Admin Only
# ==========================================================

class IsAdmin(BasePermission):
    """
    Allows access only to admins.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == CustomUser.Role.ADMIN
        )


# ==========================================================
# Hotel Manager Only
# ==========================================================

class IsHotelManager(BasePermission):
    """
    Allows access only to hotel managers.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == CustomUser.Role.HOTEL_MANAGER
        )


# ==========================================================
# Hotel Owner
# ==========================================================

class IsHotelOwnerOrReadOnly(BasePermission):
    """
    Read for everyone.
    Update/Delete only by hotel owner.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        if request.method in SAFE_METHODS:
            return True

        return obj.manager == request.user


# ==========================================================
# Booking Owner
# ==========================================================

class IsBookingOwner(BasePermission):
    """
    Only booking owner can access.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return obj.user == request.user


# ==========================================================
# Review Owner
# ==========================================================

class IsReviewOwner(BasePermission):
    """
    Only review owner can edit/delete.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


# ==========================================================
# Payment Owner
# ==========================================================

class IsPaymentOwner(BasePermission):
    """
    Only payment owner can access.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return obj.booking.user == request.user