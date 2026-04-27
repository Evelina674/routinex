from django.shortcuts import render, redirect
from .models import UserProfile, Workout, Meal, Habit, Progress

def dashboard(request):
   return render(request, "fitness/dashboard.html")

def add_workout(request):
    if request.method == "POST":
        Workout.objects.create(
            user=UserProfile.objects.first(),
            title=request.POST.get("title")
        )
    return redirect("/")

def add_meal(request):
    if request.method == "POST":
        Meal.objects.create(
            user=UserProfile.objects.first(),
            name=request.POST.get("name"),
            calories=request.POST.get("calories")
        )
    return redirect("/")

def add_habit(request):
    if request.method == "POST":
        Habit.objects.create(
            user=UserProfile.objects.first(),
            title=request.POST.get("title")
        )
    return redirect("/")

def add_progress(request):
    if request.method == "POST":
        Progress.objects.create(
            user=UserProfile.objects.first(),
            weight=request.POST.get("weight")
        )
    return redirect("/")