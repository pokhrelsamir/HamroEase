from django.urls import path

from .api_views import (
    RegisterAPIView,
    LoginAPIView,
    RefreshTokenAPIView,
    ProfileAPIView,
    ChangePasswordAPIView,
    LogoutAPIView,
)

urlpatterns = [
    # ==========================================================
    # Account Registration
    # ==========================================================
    path(
        "register/",
        RegisterAPIView.as_view(),
        name="api-register",
    ),

    # ==========================================================
    # Authentication
    # ==========================================================
    path(
        "login/",
        LoginAPIView.as_view(),
        name="api-login",
    ),

    path(
        "token/refresh/",
        RefreshTokenAPIView.as_view(),
        name="token-refresh",
    ),

    # ==========================================================
    # User Profile
    # ==========================================================
    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="api-profile",
    ),

    # ==========================================================
    # Account Security
    # ==========================================================
    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="api-change-password",
    ),

    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="api-logout",
    ),
]