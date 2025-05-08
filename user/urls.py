from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from habit.apps import HabitConfig

from .views import RegisterAPIView

app_name = HabitConfig.name

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),  # Переименуем token/ в login/ для удобства
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterAPIView.as_view(), name="register"),
]
