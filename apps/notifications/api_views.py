from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Notifications"],
        summary="My Notifications",
    ),
    retrieve=extend_schema(
        tags=["Notifications"],
        summary="Notification Details",
    ),
    destroy=extend_schema(
        tags=["Notifications"],
        summary="Delete Notification",
    ),
)
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    @extend_schema(
        tags=["Notifications"],
        summary="Mark Notification as Read",
    )
    @action(
        detail=True,
        methods=["patch"],
        url_path="read",
    )
    def mark_as_read(self, request, pk=None):

        notification = self.get_object()

        notification.is_read = True
        notification.save()

        return Response(
            {
                "detail": "Notification marked as read."
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["Notifications"],
        summary="Mark All Notifications as Read",
    )
    @action(
        detail=False,
        methods=["patch"],
        url_path="read-all",
    )
    def mark_all_as_read(self, request):

        self.get_queryset().update(
            is_read=True
        )

        return Response(
            {
                "detail": "All notifications marked as read."
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["Notifications"],
        summary="Delete Notification",
    )
    @action(
        detail=True,
        methods=["delete"],
        url_path="delete",
    )
    def delete_notification(self, request, pk=None):

        notification = self.get_object()
        notification.delete()

        return Response(
            {
                "detail": "Notification deleted successfully."
            },
            status=status.HTTP_200_OK,
        )