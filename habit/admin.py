from django.contrib import admin

from habit.models import Habit, PleasantHabit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Представляет административное представление для модели привычки.
    """

    list_display = ("user", "action")
    list_filter = ("user",)
    ordering = ("user",)


@admin.register(PleasantHabit)
class PleasantHabitAdmin(admin.ModelAdmin):
    """
    Представляет административное представление для модели приятной привычки.
    """

    list_display = ("user", "action")
    list_filter = ("user",)
    ordering = ("user",)
