from rest_framework.permissions import BasePermission


class IsReviewOwner(BasePermission):
    """
    Allows access only to the owner of the review.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsReviewOwnerOrAdmin(BasePermission):
    """
    Allows access to the review owner or an administrator.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user
            or request.user.role == "ADMIN"
        )


class CanCreateReview(BasePermission):
    """
    Allows only authenticated guests to create reviews.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "CUSTOMER"
        )