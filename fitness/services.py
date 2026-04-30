from .models import Meal, UserProfile
from django.db.models import Sum

def calculate_bmi(user):
    """Розрахунок ІМТ: weight / (height^2)"""
    profile = UserProfile.objects.get(user=user)
    if profile.height > 0:
        # Використовуємо LaTeX для формули в коментарі: $BMI = \frac{weight}{height^2}$
        return round(profile.weight / ((profile.height / 100) ** 2), 2)
    return 0

def get_daily_stats(user, date):
    total_calories = Meal.objects.filter(user=user, date=date).aggregate(Sum('calories'))['calories__sum'] or 0
    return {'total_calories': total_calories}