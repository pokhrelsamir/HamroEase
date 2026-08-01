from django.urls import path

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from .api_views import (
    RegisterAPIView,
    ProfileAPIView,
    LogoutAPIView,
    ChangePasswordAPIView,
    LoginAPIView,
    RefreshTokenAPIView,
)


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Login",
        description="Authenticate a user and obtain JWT access and refresh tokens.",
    )
)
class LoginView(TokenObtainPairView):
    pass


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Refresh Access Token",
        description="Generate a new access token using a valid refresh token.",
    )
)
class RefreshTokenView(TokenRefreshView):
    pass


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="api-login",
    ),
    path(
        "token/refresh/",
        RefreshTokenView.as_view(),
        name="token-refresh",
    ),
]