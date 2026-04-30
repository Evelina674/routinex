from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("", views.dashboard, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("add-workout/", views.add_workout, name="add_workout"),
    path("edit-workout/<int:workout_id>/", views.edit_workout, name="edit_workout"),
    path("delete-workout/<int:workout_id>/", views.delete_workout, name="delete_workout"),
    path("add-meal/", views.add_meal, name="add_meal"),
    path("add-habit/", views.add_habit, name="add_habit"),
    path("add-progress/", views.add_progress, name="add_progress"),
    path("add-exercise/<int:workout_id>/", views.add_exercise, name="add_exercise"),
    path("workouts/", views.workout_list, name="workout_list"),
    path("workout/<int:workout_id>/", views.workout_detail, name="workout_detail"),
]