from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import HotelViewSet, RoomViewSet


router = DefaultRouter()

router.register(
    "hotels",
    HotelViewSet,
    basename="api-hotels"
)

router.register(
    "rooms",
    RoomViewSet,
    basename="api-rooms"
)


urlpatterns = [
    path("", include(router.urls)),
]