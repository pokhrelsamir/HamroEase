from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Login",
        description="Authenticate a user and obtain JWT access and refresh tokens.",
    )
)
class LoginAPIView(TokenObtainPairView):
    pass


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Refresh Access Token",
        description="Generate a new access token using a valid refresh token.",
    )
)
class RefreshTokenAPIView(TokenRefreshView):
    pass