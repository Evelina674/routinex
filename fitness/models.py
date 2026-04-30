from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    goal = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    reps = models.IntegerField()
    sets = models.IntegerField()


class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    done = models.BooleanField(default=False)


# 🟢 ПРОГРЕС (ОЦЕ ТИ ХОТІВ)
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.weight}"