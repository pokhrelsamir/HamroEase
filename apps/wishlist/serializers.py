from rest_framework import serializers

from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):

    hotel_name = serializers.CharField(
        source="hotel.name",
        read_only=True,
    )

    hotel_city = serializers.CharField(
        source="hotel.city",
        read_only=True,
    )

    hotel_country = serializers.CharField(
        source="hotel.country",
        read_only=True,
    )

    hotel_thumbnail = serializers.ImageField(
        source="hotel.thumbnail",
        read_only=True,
    )

    class Meta:
        model = Wishlist

        fields = (
            "id",
            "hotel",
            "hotel_name",
            "hotel_city",
            "hotel_country",
            "hotel_thumbnail",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
        )

    def validate(self, attrs):

        user = self.context["request"].user
        hotel = attrs["hotel"]

        if Wishlist.objects.filter(
            user=user,
            hotel=hotel,
        ).exists():

            raise serializers.ValidationError(
                "Hotel is already in your wishlist."
            )

        return attrs

    def create(self, validated_data):

        return Wishlist.objects.create(
            user=self.context["request"].user,
            **validated_data,
        )