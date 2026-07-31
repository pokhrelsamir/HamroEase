from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    password_confirm = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "full_name",
            "role",
            "phone_number",
            "profile_picture",
            "password",
            "password_confirm",
        )

    def validate(self, attrs):

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {
                    "password": "Passwords do not match."
                }
            )

        return attrs

    def create(self, validated_data):

        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = CustomUser(**validated_data)

        user.set_password(password)

        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = (
            "id",
            "email",
            "full_name",
            "role",
            "phone_number",
            "profile_picture",
        )


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        required=True
    )

    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
    )