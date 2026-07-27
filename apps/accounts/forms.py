from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "full_name",
            "email",
            "phone_number",
            "profile_picture",
            "password1",
            "password2",
        )

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )

    def save(self, commit=True):
        user = super().save(commit=False)

        # Every new user becomes a Guest
        user.role = CustomUser.Role.GUEST

        if commit:
            user.save()

        return user