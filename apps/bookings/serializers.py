from django.db.models import Q
from django.utils import timezone

from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = "__all__"

        read_only_fields = (
            "id",
            "user",
            "created_at",
            "updated_at",
            "total_nights",
            "total_price",
        )

    def validate(self, attrs):

        room = attrs.get("room")
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")

        # ----------------------------------------------------------
        # Room under maintenance
        # ----------------------------------------------------------

        if room and room.status == "maintenance":
            raise serializers.ValidationError(
                {
                    "room": (
                        "This room is currently under maintenance "
                        "and cannot be booked."
                    )
                }
            )

        # ----------------------------------------------------------
        # Prevent booking in the past
        # ----------------------------------------------------------

        today = timezone.localdate()

        if check_in and check_in < today:
            raise serializers.ValidationError(
                {
                    "check_in": "Check-in date cannot be in the past."
                }
            )

        # ----------------------------------------------------------
        # Check-in / Check-out validation
        # ----------------------------------------------------------

        if check_in and check_out:

            if check_in >= check_out:
                raise serializers.ValidationError(
                    {
                        "check_out": (
                            "Check-out date must be after check-in date."
                        )
                    }
                )

        # ----------------------------------------------------------
        # Prevent overlapping bookings
        # ----------------------------------------------------------

        if room and check_in and check_out:

            overlapping_booking = Booking.objects.filter(
                room=room,
                status__in=[
                    Booking.Status.PENDING,
                    Booking.Status.CONFIRMED,
                    Booking.Status.CHECKED_IN,
                ],
            ).filter(
                Q(check_in__lt=check_out)
                & Q(check_out__gt=check_in)
            )

            # Ignore current booking while updating
            if self.instance:
                overlapping_booking = overlapping_booking.exclude(
                    pk=self.instance.pk
                )

            if overlapping_booking.exists():
                raise serializers.ValidationError(
                    {
                        "room": (
                            "This room is already booked for the selected dates."
                        )
                    }
                )

        return attrs

    
# from django.db.models import Q
# from rest_framework import serializers

# from .models import Booking


# class BookingSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Booking
#         fields = "__all__"
        
#         read_only_fields = (
#         "id",
#         "user",
#         "created_at",
#         "updated_at",
#         "total_nights",
#         "total_price",
#     )

#     def validate(self, attrs):

#         room = attrs.get("room")
#         check_in = attrs.get("check_in")
#         check_out = attrs.get("check_out")

#         if room and check_in and check_out:

#             overlapping_booking = Booking.objects.filter(
#                 room=room,
#                 status__in=[
#                     Booking.Status.PENDING,
#                     Booking.Status.CONFIRMED,
#                     Booking.Status.CHECKED_IN,
#                 ],
#             ).filter(
#                 Q(check_in__lt=check_out) &
#                 Q(check_out__gt=check_in)
#             )

#             # Ignore the current booking when updating
#             if self.instance:
#                 overlapping_booking = overlapping_booking.exclude(
#                     pk=self.instance.pk
#                 )

#             if overlapping_booking.exists():
#                 raise serializers.ValidationError(
#                     {
#                         "room": "This room is already booked for the selected dates."
#                     }
#                 )

#         return attrs