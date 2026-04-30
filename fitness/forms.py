from django import forms
from .models import Workout, Meal, Habit, Progress


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["title"]


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["name", "calories"]


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["title", "is_done"]


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ["weight"]