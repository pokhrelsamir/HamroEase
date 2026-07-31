from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .api_views import BookingViewSet


router = DefaultRouter()

router.register(
    "bookings",
    BookingViewSet,
    basename="bookings",
)

urlpatterns = [
    path("", include(router.urls)),
]