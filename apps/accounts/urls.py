from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("guest-dashboard/", views.guest_dashboard, name="guest_dashboard"),
    path("manager-dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("profile/", views.profile, name="profile",
),
]