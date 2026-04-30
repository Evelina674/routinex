from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import UserProfile, Workout, Exercise, Meal, Habit, Progress, WorkoutComment, WorkoutLike
from .forms import ProfileForm, WorkoutForm, ExerciseForm, MealForm, HabitForm, ProgressForm, CommentForm


# 📝 SIGNUP
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")


# 🧠 DASHBOARD
@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    today = timezone.localdate()

    workout_list = Workout.objects.filter(user=request.user).order_by("-date", "-created_at")
    today_workouts = workout_list.filter(date=today)
    meals = Meal.objects.filter(user=request.user).order_by("-date")
    habits = Habit.objects.filter(user=request.user)
    progress = Progress.objects.filter(user=request.user).order_by("-date")

    return render(request, "fitness/dashboard.html", {
        "profile": profile,
        "today_workouts": today_workouts,
        "history_workouts": workout_list,
        "meals": meals[:5],
        "habits": habits,
        "progress": progress[:5],
        "today": today,
    })


# 🧑‍💼 PROFILE
@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "fitness/profile.html", {
        "profile": profile,
        "form": form,
    })


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "fitness/edit_profile.html", {"form": form})


# 🏋️ WORKOUT
@login_required
def add_workout(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect("workout_detail", workout_id=workout.id)
    else:
        form = WorkoutForm()

    return render(request, "fitness/add_workout.html", {"form": form})


@login_required
def edit_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    if request.method == "POST":
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect("workout_detail", workout_id=workout.id)
    else:
        form = WorkoutForm(instance=workout)

    return render(request, "fitness/edit_workout.html", {"form": form, "workout": workout})


@login_required
def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    if request.method == "POST":
        workout.delete()
        return redirect("dashboard")

    return render(request, "fitness/delete_workout.html", {"workout": workout})


# ➕ EXERCISE
@login_required
def add_exercise(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.workout = workout
            exercise.save()
            return redirect("workout_detail", workout_id=workout.id)
    else:
        form = ExerciseForm()

    return render(request, "fitness/add_exercise.html", {"workout": workout, "form": form})


# 🍽 MEAL
@login_required
def add_meal(request):
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect("dashboard")
    else:
        form = MealForm()

    return render(request, "fitness/add_meal.html", {"form": form})


# 🔁 HABIT
@login_required
def add_habit(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect("dashboard")
    else:
        form = HabitForm()

    return render(request, "fitness/add_habit.html", {"form": form})


@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user).order_by("-date", "-created_at")
    return render(request, "fitness/workout_list.html", {"workouts": workouts})


@login_required
def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    is_owner = workout.user == request.user
    comments = workout.comments.order_by("created_at")
    liked = WorkoutLike.objects.filter(workout=workout, user=request.user).exists()

    if request.method == "POST":
        if "like" in request.POST:
            like, created = WorkoutLike.objects.get_or_create(workout=workout, user=request.user)
            if not created:
                like.delete()
            return redirect("workout_detail", workout_id=workout.id)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.workout = workout
                comment.user = request.user
                comment.save()
                return redirect("workout_detail", workout_id=workout.id)
    else:
        form = CommentForm()

    return render(request, "fitness/workout_detail.html", {
        "workout": workout,
        "exercises": workout.exercises.all(),
        "comments": comments,
        "liked": liked,
        "likes_count": workout.likes.count(),
        "form": form,
        "is_owner": is_owner,
    })


@login_required
def add_progress(request):
    if request.method == "POST":
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.save()
            return redirect("dashboard")
    else:
        form = ProgressForm()

    return render(request, "fitness/add_progress.html", {"form": form})