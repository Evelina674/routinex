from django.db import models

class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    weight = models.FloatField()
    height = models.FloatField()
    goal = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class Workout(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField()

class Meal(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    date = models.DateTimeField()

class Habit(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    date = models.DateField()

class Progress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    weight_record = models.FloatField()
    date = models.DateField()