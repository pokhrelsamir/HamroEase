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
)
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Notification API

    GET     /api/notifications/
    PATCH   /api/notifications/{id}/read/
    PATCH   /api/notifications/read-all/
    DELETE  /api/notifications/clear/
    """

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

    @extend_schema(
        tags=["Notifications"],
        summary="Mark Notification as Read",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Notification marked as read.",
                    }
                },
            }
        },
    )
    @action(
        detail=True,
        methods=["patch"],
        url_path="read",
    )
    def read(self, request, pk=None):

        notification = self.get_object()

        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])

        return Response(
            {
                "detail": "Notification marked as read."
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["Notifications"],
        summary="Mark All Notifications as Read",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "All notifications marked as read.",
                    }
                },
            }
        },
    )
    @action(
        detail=False,
        methods=["patch"],
        url_path="read-all",
    )
    def read_all(self, request):

        self.get_queryset().filter(
            is_read=False
        ).update(is_read=True)

        return Response(
            {
                "detail": "All notifications marked as read."
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        tags=["Notifications"],
        summary="Clear All Notifications",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "All notifications deleted.",
                    }
                },
            }
        },
    )
    @action(
        detail=False,
        methods=["delete"],
        url_path="clear",
    )
    def clear(self, request):

        self.get_queryset().delete()

        return Response(
            {
                "detail": "All notifications deleted."
            },
            status=status.HTTP_200_OK,
        )