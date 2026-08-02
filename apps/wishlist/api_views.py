from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Wishlist
from .serializers import WishlistSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Wishlist"],
        summary="My Wishlist",
    ),
    retrieve=extend_schema(
        tags=["Wishlist"],
        summary="Wishlist Details",
    ),
    create=extend_schema(
        tags=["Wishlist"],
        summary="Add Hotel to Wishlist",
    ),
    destroy=extend_schema(
        tags=["Wishlist"],
        summary="Remove Hotel from Wishlist",
    ),
)
class WishlistViewSet(viewsets.ModelViewSet):

    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(
            user=self.request.user
        ).select_related("hotel")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):

        wishlist = self.get_object()
        wishlist.delete()

        return Response(
            {
                "detail": "Hotel removed from wishlist successfully."
            },
            status=status.HTTP_200_OK,
        )