from rest_framework import serializers

from apps.bookings.models import Booking

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "booking",
            "hotel",
            "user",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "hotel",
            "user",
            "created_at",
            "updated_at",
        ]

    def validate_booking(self, booking):
        request = self.context["request"]

        if booking.user != request.user:
            raise serializers.ValidationError(
                "You can only review your own booking."
            )

        if booking.status != Booking.Status.CHECKED_OUT:
            raise serializers.ValidationError(
                "You can only review completed bookings."
            )

        if hasattr(booking, "review"):
            raise serializers.ValidationError(
                "This booking has already been reviewed."
            )

        return booking

    def create(self, validated_data):
        booking = validated_data["booking"]

        return Review.objects.create(
            booking=booking,
            hotel=booking.room.hotel,
            user=self.context["request"].user,
            rating=validated_data["rating"],
            comment=validated_data.get("comment", ""),
        )