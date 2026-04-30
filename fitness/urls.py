from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("add-workout/", views.add_workout),
    path("add-meal/", views.add_meal),
    path("add-habit/", views.add_habit),
    path("add-exercise/<int:workout_id>/", views.add_exercise),
]