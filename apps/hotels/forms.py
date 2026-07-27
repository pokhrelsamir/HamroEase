from django import forms

from .models import (
    Hotel,
    Room,
)


# ======================================================
# Hotel Form
# ======================================================

class HotelForm(forms.ModelForm):

    class Meta:

        model = Hotel

        exclude = (
            "manager",
            "created_at",
            "updated_at",
        )

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "thumbnail": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "star_rating": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "amenities": forms.SelectMultiple(
                attrs={
                    "class": "form-select"
                }
            ),

            "check_in_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "check_out_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }


# ======================================================
# Room Form
# ======================================================

class RoomForm(forms.ModelForm):

    class Meta:

        model = Room

        fields = "__all__"

        widgets = {

            "hotel": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "room_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "room_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "price_per_night": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "max_guests": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "total_beds": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "room_size": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "main_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "amenities": forms.SelectMultiple(
                attrs={
                    "class": "form-select"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }