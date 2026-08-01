from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .serializers import ReviewSerializer
from .permissions import (
    IsReviewOwnerOrAdmin,
    CanCreateReview,
)


@extend_schema_view(
    list=extend_schema(
        tags=["Reviews"],
        summary="List Reviews",
    ),
    retrieve=extend_schema(
        tags=["Reviews"],
        summary="Review Details",
    ),
    create=extend_schema(
        tags=["Reviews"],
        summary="Create Review",
    ),
    update=extend_schema(
        tags=["Reviews"],
        summary="Update Review",
    ),
    partial_update=extend_schema(
        tags=["Reviews"],
        summary="Partial Update Review",
    ),
    destroy=extend_schema(
        tags=["Reviews"],
        summary="Delete Review",
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.select_related(
        "user",
        "hotel",
        "booking",
    )

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return self.queryset

        if user.role == "HOTEL_MANAGER":
            return self.queryset.filter(
                hotel__owner=user
            )

        return self.queryset.filter(
            user=user
        )

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [
                IsAuthenticated,
                CanCreateReview,
            ]
        elif self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [
                IsAuthenticated,
                IsReviewOwnerOrAdmin,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
            ]

        return [
            permission()
            for permission in permission_classes
        ]