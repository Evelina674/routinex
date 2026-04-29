from django import forms
from .models import Workout, Meal, HabitLog, Progress


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["title", "description", "is_public"]


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["name", "calories"]


class HabitForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ["date", "water_liters", "sleep_hours", "steps"]


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ["date", "weight"]