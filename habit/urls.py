from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .apps import HabitConfig
from .views import HabitViewSet

app_name = HabitConfig.name

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")

urlpatterns = [
    path("", include(router.urls)),
]
