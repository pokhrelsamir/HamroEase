from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):

    user = request.user

    if user.role == "HOTEL_MANAGER":
        template = "dashboard/manager_dashboard.html"

    elif user.role == "ADMIN":
        template = "dashboard/admin_dashboard.html"

    else:
        template = "dashboard/guest_dashboard.html"

    return render(request, template)