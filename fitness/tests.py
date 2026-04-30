from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import UserProfile, Workout, Exercise, Meal, Habit, Progress
from .forms import ProfileForm, WorkoutForm, MealForm, HabitForm, ProgressForm


class ModelStrTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass1234')

    def test_userprofile_str(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.assertEqual(str(profile), 'tester')

    def test_workout_str(self):
        workout = Workout.objects.create(user=self.user, title='Morning', date=timezone.localdate())
        self.assertEqual(str(workout), 'Morning')

    def test_exercise_str(self):
        workout = Workout.objects.create(user=self.user, title='Train', date=timezone.localdate())
        exercise = Exercise.objects.create(workout=workout, name='Push-up', reps=10, sets=3)
        self.assertEqual(str(exercise), 'Push-up')

    def test_meal_str(self):
        meal = Meal.objects.create(user=self.user, name='Salad', calories=200, date=timezone.localdate())
        self.assertEqual(str(meal), 'Salad')

    def test_habit_str(self):
        habit = Habit.objects.create(user=self.user, name='Meditation', category='routine')
        self.assertEqual(str(habit), 'Meditation')

    def test_progress_str(self):
        progress = Progress.objects.create(user=self.user, weight=70.5, date=timezone.localdate())
        self.assertEqual(str(progress), 'tester - 70.5')


class AuthTests(TestCase):
    def setUp(self):
        self.username = 'tester'
        self.password = 'pass1234'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_signup_page_status_code(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_creates_user(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
        })
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_login_redirects_dashboard(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_logout_redirects_login(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_dashboard_redirects_anonymous(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_profile_redirects_anonymous(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)


class FitnessViewTests(TestCase):
    def setUp(self):
        self.username = 'tester'
        self.password = 'pass1234'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_profile_page_status_code_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page_status_code_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_add_workout_page_status_code_logged_in(self):
        response = self.client.get(reverse('add_workout'))
        self.assertEqual(response.status_code, 200)

    def test_add_workout_creates_workout(self):
        response = self.client.post(reverse('add_workout'), {
            'title': 'Evening',
            'category': 'strength',
            'date': timezone.localdate(),
            'note': 'Great session',
        })
        self.assertEqual(Workout.objects.filter(user=self.user, title='Evening').count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_workout_list_view_contains_workout(self):
        workout = Workout.objects.create(user=self.user, title='Plan', date=timezone.localdate())
        response = self.client.get(reverse('workout_list'))
        self.assertContains(response, workout.title)

    def test_workout_detail_view_contains_workout_title(self):
        workout = Workout.objects.create(user=self.user, title='Focus', date=timezone.localdate())
        response = self.client.get(reverse('workout_detail', args=[workout.id]))
        self.assertContains(response, workout.title)

    def test_edit_workout_updates_workout(self):
        workout = Workout.objects.create(user=self.user, title='Old', date=timezone.localdate())
        response = self.client.post(reverse('edit_workout', args=[workout.id]), {
            'title': 'Updated',
            'category': 'cardio',
            'date': timezone.localdate(),
            'note': 'Updated note',
        })
        workout.refresh_from_db()
        self.assertEqual(workout.title, 'Updated')
        self.assertEqual(response.status_code, 302)

    def test_delete_workout_removes_workout(self):
        workout = Workout.objects.create(user=self.user, title='Remove', date=timezone.localdate())
        response = self.client.post(reverse('delete_workout', args=[workout.id]))
        self.assertFalse(Workout.objects.filter(id=workout.id).exists())
        self.assertEqual(response.status_code, 302)

    def test_add_exercise_to_workout(self):
        workout = Workout.objects.create(user=self.user, title='Build', date=timezone.localdate())
        response = self.client.post(reverse('add_exercise', args=[workout.id]), {
            'name': 'Squat',
            'reps': 12,
            'sets': 4,
        })
        self.assertEqual(workout.exercises.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_add_meal_creates_meal(self):
        response = self.client.post(reverse('add_meal'), {
            'name': 'Oatmeal',
            'calories': 250,
            'date': timezone.localdate(),
        })
        self.assertEqual(Meal.objects.filter(user=self.user, name='Oatmeal').count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_add_habit_creates_habit(self):
        response = self.client.post(reverse('add_habit'), {
            'name': 'Stretching',
            'category': 'health',
        })
        self.assertEqual(Habit.objects.filter(user=self.user, name='Stretching').count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_add_progress_creates_progress(self):
        response = self.client.post(reverse('add_progress'), {
            'weight': 68.0,
            'date': timezone.localdate(),
        })
        self.assertEqual(Progress.objects.filter(user=self.user, weight=68.0).count(), 1)
        self.assertEqual(response.status_code, 302)


class FormValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)

    def test_profile_form_invalid_without_height(self):
        form = ProfileForm(data={
            'weight': 60,
            'goal': 'Stay fit',
            'is_public': True,
        }, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('height', form.errors)

    def test_workout_form_invalid_without_title(self):
        form = WorkoutForm(data={
            'category': 'strength',
            'date': timezone.localdate(),
            'note': 'No title',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_meal_form_invalid_without_name(self):
        form = MealForm(data={
            'calories': 200,
            'date': timezone.localdate(),
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_habit_form_invalid_without_name(self):
        form = HabitForm(data={
            'category': 'health',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_progress_form_invalid_without_weight(self):
        form = ProgressForm(data={
            'date': timezone.localdate(),
        })
        self.assertFalse(form.is_valid())
        self.assertIn('weight', form.errors)

    def test_workout_form_valid_with_all_fields(self):
        form = WorkoutForm(data={
            'title': 'Valid',
            'category': 'cardio',
            'date': timezone.localdate(),
            'note': 'Okay',
        })
        self.assertTrue(form.is_valid())
