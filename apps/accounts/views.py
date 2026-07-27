from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import RegisterForm, LoginForm
from .models import CustomUser


# ==========================
# User Registration
# ==========================
def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Registration completed successfully. Please login."
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


# ==========================
# User Login
# ==========================
def login_view(request):

    # If user is already logged in
    if request.user.is_authenticated:

        if request.user.role == CustomUser.Role.ADMIN:
            return redirect("admin_dashboard")

        elif request.user.role == CustomUser.Role.HOTEL_MANAGER:
            return redirect("manager_dashboard")

        return redirect("guest_dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # IMPORTANT:
            # Use username=email because USERNAME_FIELD = "email"
            user = authenticate(
                request,
                username=email,
                password=password,
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    f"Welcome back, {user.full_name}!"
                )

                if user.role == CustomUser.Role.ADMIN:
                    return redirect("admin_dashboard")

                elif user.role == CustomUser.Role.HOTEL_MANAGER:
                    return redirect("manager_dashboard")

                return redirect("guest_dashboard")

            else:

                messages.error(
                    request,
                    "Invalid email or password."
                )

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


# ==========================
# Logout
# ==========================
@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


# ==========================
# Temporary Dashboards
# ==========================
@login_required
def guest_dashboard(request):
    return HttpResponse("<h1>Guest Dashboard</h1>")


@login_required
def manager_dashboard(request):
    return HttpResponse("<h1>Hotel Manager Dashboard</h1>")


@login_required
def admin_dashboard(request):
    return HttpResponse("<h1>Admin Dashboard</h1>")

@login_required
def profile(request):

    return render(
        request,
        "accounts/profile.html",
    )