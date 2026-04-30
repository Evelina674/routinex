from django.contrib import admin
from .models import UserProfile, Workout, Exercise, Meal, Habit, Progress

admin.site.register(UserProfile)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Meal)
admin.site.register(Habit)
admin.site.register(Progress)