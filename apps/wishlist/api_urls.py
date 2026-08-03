from rest_framework.routers import DefaultRouter
from .api_views import WishlistViewSet

router = DefaultRouter()

router.register(
    "wishlist",
    WishlistViewSet,
    basename="wishlist",
)

urlpatterns = router.urls