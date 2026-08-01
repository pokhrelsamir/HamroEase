from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Payment
from .serializers import PaymentSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["Payments"],
        summary="List Payments",
    ),
    retrieve=extend_schema(
        tags=["Payments"],
        summary="Payment Details",
    ),
    create=extend_schema(
        tags=["Payments"],
        summary="Create Payment",
    ),
    update=extend_schema(
        tags=["Payments"],
        summary="Update Payment",
    ),
    partial_update=extend_schema(
        tags=["Payments"],
        summary="Partial Update Payment",
    ),
    destroy=extend_schema(
        tags=["Payments"],
        summary="Delete Payment",
    ),
)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]