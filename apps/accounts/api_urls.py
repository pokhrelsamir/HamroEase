from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .api_views import (
    RegisterAPIView,
    ProfileAPIView,
    LogoutAPIView,
    ChangePasswordAPIView,
)

urlpatterns = [

    # Register
    path("register/", RegisterAPIView.as_view(), name="api-register"),

    # Login
    path("login/", TokenObtainPairView.as_view(), name="api-login"),

    # Refresh Token
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    # Profile
    path("profile/", ProfileAPIView.as_view(), name="api-profile"),

    # Logout
    path("logout/", LogoutAPIView.as_view(), name="api-logout"),

    # Change Password
    path( "change-password/", ChangePasswordAPIView.as_view(), name="api-change-password" ),
]