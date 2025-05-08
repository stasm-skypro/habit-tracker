from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Представляет административное представление для модели пользователя.
    """

    list_display = ("email", "first_name", "last_name")
    search_fields = ("email",)
    ordering = ("email",)
