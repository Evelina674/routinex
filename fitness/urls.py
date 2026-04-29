from django.urls import path
from .views import dashboard, add_workout, add_meal, add_habit, add_progress

urlpatterns = [
    path("", dashboard),
    path("workout/add/", add_workout),
    path("meal/add/", add_meal),
    path("habit/add/", add_habit),
    path("progress/add/", add_progress),
]