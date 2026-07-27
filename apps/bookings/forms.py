from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = (
            "hotel",
            "room",
            "check_in",
            "check_out",
            "guests",
            "special_request",
        )

        widgets = {

            "hotel": forms.Select(
                attrs={"class": "form-select"}
            ),

            "room": forms.Select(
                attrs={"class": "form-select"}
            ),

            "check_in": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "check_out": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "guests": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),

            "special_request": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Any special requests...",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        room = cleaned_data.get("room")
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        guests = cleaned_data.get("guests")

        # -----------------------------------------
        # Check-in date cannot be in the past
        # -----------------------------------------
        if check_in and check_in < date.today():
            raise ValidationError(
                "Check-in date cannot be in the past."
            )

        # -----------------------------------------
        # Check-out must be after check-in
        # -----------------------------------------
        if check_in and check_out:

            if check_out <= check_in:
                raise ValidationError(
                    "Check-out date must be after check-in."
                )

        # -----------------------------------------
        # Room guest capacity validation
        # -----------------------------------------
        if room and guests:

            if guests > room.max_guests:
                raise ValidationError(
                    f"This room allows only {room.max_guests} guests."
                )

        # -----------------------------------------
        # Prevent double booking
        # -----------------------------------------
        if room and check_in and check_out:

            overlapping_booking = Booking.objects.filter(
                room=room
            ).filter(
                Q(check_in__lt=check_out) &
                Q(check_out__gt=check_in)
            ).exclude(
                status="cancelled"
            )

            # Ignore current booking while editing
            if self.instance.pk:
                overlapping_booking = overlapping_booking.exclude(
                    pk=self.instance.pk
                )

            if overlapping_booking.exists():
                raise ValidationError(
                    "This room is already booked for the selected dates."
                )

        return cleaned_data