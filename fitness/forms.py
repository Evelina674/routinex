from django import forms
from .models import Workout, Meal, Habit, Progress, Exercise, UserProfile, WorkoutComment


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["weight", "height", "goal", "is_public"]
        widgets = {
            "weight": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "height": forms.NumberInput(attrs={"class": "form-control"}),
            "goal": forms.TextInput(attrs={"class": "form-control"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["title", "category", "date", "note"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Назва тренування"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Короткий опис..."}),
        }


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "reps", "sets"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Назва вправи"}),
            "reps": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "sets": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["name", "calories", "date"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Страва або перекус"}),
            "calories": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Назва звички"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ["weight", "date"]
        widgets = {
            "weight": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = WorkoutComment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Написати коментар"}),
        }
        labels = {
            "text": "Коментар",
        }