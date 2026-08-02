from rest_framework.routers import DefaultRouter

from .api_views import WishlistViewSet

router = DefaultRouter()
router.register(
    "",
    WishlistViewSet,
    basename="wishlist",
)

urlpatterns = router.urls