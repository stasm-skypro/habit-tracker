"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version="v1",
        description="Документация к API трекера привычек",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="stasm226@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/habit/", include("habit.urls", namespace="habit")),
    # Swagger and Redoc
    path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
