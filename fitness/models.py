from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    goal = models.CharField(max_length=255, blank=True)
    is_public = models.BooleanField(default=True)
    friends = models.ManyToManyField("self", blank=True, symmetrical=True)

    def __str__(self):
        return self.user.username


class Workout(models.Model):
    CATEGORY_CHOICES = [
        ("strength", "Силове"),
        ("cardio", "Кардіо"),
        ("group", "Групове заняття"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="strength")
    date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=255)
    reps = models.IntegerField()
    sets = models.IntegerField()

    def __str__(self):
        return self.name


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return self.name


class Habit(models.Model):
    CATEGORY_CHOICES = [
        ("health", "Здоров'я"),
        ("routine", "Рутина"),
        ("other", "Інше"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="routine")
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f"{self.user.username} - {self.weight}"


class WorkoutComment(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"


class WorkoutLike(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("workout", "user")

    def __str__(self):
        return f"{self.user.username} likes {self.workout.title}"
