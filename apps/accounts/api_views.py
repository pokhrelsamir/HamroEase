from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ChangePasswordSerializer,
)


# ==========================================================
# Register
# ==========================================================

@extend_schema(
    tags=["Authentication"],
    summary="Register User",
    description="Create a new user account.",
)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# ==========================================================
# Login
# ==========================================================

@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Login",
        description="Authenticate a user and return JWT access and refresh tokens.",
    )
)
class LoginAPIView(TokenObtainPairView):
    pass


# ==========================================================
# Refresh Token
# ==========================================================

@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Refresh Access Token",
        description="Generate a new access token using a valid refresh token.",
    )
)
class RefreshTokenAPIView(TokenRefreshView):
    pass


# ==========================================================
# User Profile
# ==========================================================

@extend_schema_view(
    get=extend_schema(
        tags=["Authentication"],
        summary="View Profile",
    ),
    put=extend_schema(
        tags=["Authentication"],
        summary="Update Profile",
    ),
    patch=extend_schema(
        tags=["Authentication"],
        summary="Partial Update Profile",
    ),
)
class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ==========================================================
# Logout
# ==========================================================

@extend_schema(
    tags=["Authentication"],
    summary="Logout User",
    description="Logout the current user by blacklisting the refresh token.",
)
class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "detail": "Logged out successfully."
                }
            )

        except Exception:
            return Response(
                {
                    "detail": "Invalid refresh token."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# ==========================================================
# Change Password
# ==========================================================

@extend_schema(
    tags=["Authentication"],
    summary="Change Password",
    description="Change the password of the authenticated user.",
)
class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            if not user.check_password(
                serializer.validated_data["old_password"]
            ):
                return Response(
                    {
                        "old_password": "Wrong password."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(
                serializer.validated_data["new_password"]
            )
            user.save()

            return Response(
                {
                    "detail": "Password changed successfully."
                }
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )