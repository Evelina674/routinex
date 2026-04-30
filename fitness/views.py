from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import UserProfile, Workout, Exercise, Meal, Habit, Progress


# 🧠 DASHBOARD
@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    workouts = Workout.objects.filter(user=request.user)
    meals = Meal.objects.filter(user=request.user)
    habits = Habit.objects.filter(user=request.user)

    return render(request, "fitness/dashboard.html", {
        "profile": profile,
        "workouts": workouts,
        "meals": meals,
        "habits": habits
    })


# 🧠 PROFILE
@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.weight = request.POST.get("weight") or 0
        profile.height = request.POST.get("height") or 0
        profile.goal = request.POST.get("goal") or ""
        profile.save()
        return redirect("dashboard")

    return render(request, "fitness/edit_profile.html", {"profile": profile})


# 🏋️ WORKOUT
@login_required
def add_workout(request):
    if request.method == "POST":
        Workout.objects.create(
            user=request.user,
            title=request.POST.get("title")
        )
        return redirect("dashboard")

    return render(request, "fitness/add_workout.html")


# ➕ EXERCISE
@login_required
def add_exercise(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)

    if request.method == "POST":
        Exercise.objects.create(
            workout=workout,
            name=request.POST.get("name"),
            reps=request.POST.get("reps"),
            sets=request.POST.get("sets")
        )
        return redirect("dashboard")

    return render(request, "fitness/add_exercise.html", {"workout": workout})


# 🍽 MEAL
@login_required
def add_meal(request):
    if request.method == "POST":
        Meal.objects.create(
            user=request.user,
            name=request.POST.get("name"),
            calories=request.POST.get("calories")
        )
        return redirect("dashboard")

    return render(request, "fitness/add_meal.html")


# 🔁 HABIT
@login_required
def add_habit(request):
    if request.method == "POST":
        Habit.objects.create(
            user=request.user,
            name=request.POST.get("name")
        )
        return redirect("dashboard")

    return render(request, "fitness/add_habit.html")

@login_required
def add_progress(request):
    if request.method == "POST":
        Progress.objects.create(
            user=request.user,
            weight=request.POST.get("weight")
        )
        return redirect("dashboard")

    return render(request, "fitness/add_progress.html")