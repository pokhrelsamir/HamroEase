from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Admin Panel
    path("admin/", admin.site.urls),

    # Authentication
    path("accounts/", include("apps.accounts.urls")),

    # Hotel Management
    path("hotels/", include("apps.hotels.urls")),

    # Bookings
    path("bookings/", include("apps.bookings.urls")),

    # API Routes
    path("api/", include("apps.api.urls")),

    #Accounts API
    path("api/auth/", include("apps.accounts.api_urls")),

    # Hotels API
    path("api/", include("apps.hotels.api_urls")),

    # Booking API
    path("api/", include("apps.bookings.api_urls")),

    #Payments API
    path("api/", include("apps.payments.api_urls")),

    # Reviews API
    path("api/", include("apps.reviews.api_urls")),
    
    # Wishlist API
    path("api/", include("apps.wishlist.api_urls")),

    # API Documentation
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "swagger/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),

    path(
        "redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )


# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
#     SpectacularRedocView,
# )


# urlpatterns = [
#     # Admin Panel
#     path("admin/", admin.site.urls),

#     # Authentication
#     path("accounts/", include("apps.accounts.urls")),

#     # Hotel Management
#     path("hotels/", include("apps.hotels.urls")),

#     # Bookings
#     path("bookings/", include("apps.bookings.urls")),

#     # API Routes
#     path("api/", include("apps.api.urls")),

#     # API Documentation
#     path(
#         "api/schema/",
#         SpectacularAPIView.as_view(),
#         name="schema"
#     ),

#     path(
#         "api/docs/",
#         SpectacularSwaggerView.as_view(
#             url_name="schema"
#         ),
#         name="swagger-ui"
#     ),

#     path(
#         "api/redoc/",
#         SpectacularRedocView.as_view(
#             url_name="schema"
#         ),
#         name="redoc"
#     ),
# ]


# # Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT
#     )


# # Serve static files during development
# if settings.DEBUG:
#     urlpatterns += static(
#         settings.STATIC_URL,
#         document_root=settings.STATIC_ROOT
#     )


# # from django.contrib import admin
# # from django.urls import path, include
# # from django.conf import settings
# # from django.conf.urls.static import static

# # urlpatterns = [
# #     # Admin Panel
# #     path("admin/", admin.site.urls),

# #     # Authentication
# #     path("accounts/", include("apps.accounts.urls")),

# #     # Hotel Management
# #     path("hotels/", include("apps.hotels.urls")),

# #     # Bookings
# #     path("bookings/", include("apps.bookings.urls")),
# # ]

# # # Serve media files during development
# # if settings.DEBUG:
# #     urlpatterns += static(
# #         settings.MEDIA_URL,
# #         document_root=settings.MEDIA_ROOT
# #     )

# # # (Optional) Serve static files during development
# # if settings.DEBUG:
# #     urlpatterns += static(
# #         settings.STATIC_URL,
# #         document_root=settings.STATIC_ROOT
# #     )