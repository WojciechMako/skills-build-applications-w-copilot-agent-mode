from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from django.db import models as dj_models

class Team(dj_models.Model):
    name = dj_models.CharField(max_length=100, unique=True)

class Activity(dj_models.Model):
    user = dj_models.ForeignKey('auth.User', on_delete=dj_models.CASCADE)
    type = dj_models.CharField(max_length=50)
    duration = dj_models.IntegerField()

class Workout(dj_models.Model):
    name = dj_models.CharField(max_length=100)
    description = dj_models.TextField()
    suggested_for_team = dj_models.ForeignKey(Team, on_delete=dj_models.CASCADE)

class Leaderboard(dj_models.Model):
    user = dj_models.ForeignKey('auth.User', on_delete=dj_models.CASCADE)
    points = dj_models.IntegerField()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Usuń istniejące dane
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Dodaj drużyny
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Dodaj użytkowników
        users = [
            User(email='ironman@marvel.com', username='ironman'),
            User(email='captain@marvel.com', username='captain'),
            User(email='batman@dc.com', username='batman'),
            User(email='superman@dc.com', username='superman'),
        ]
        for i, user in enumerate(users):
            user.set_password('password')
            user.save()
            if i < 2:
                user.team = marvel
            else:
                user.team = dc
            user.save()

        # Dodaj aktywności
        Activity.objects.create(user=users[0], type='run', duration=30)
        Activity.objects.create(user=users[1], type='cycle', duration=45)
        Activity.objects.create(user=users[2], type='swim', duration=25)
        Activity.objects.create(user=users[3], type='run', duration=60)

        # Dodaj treningi
        Workout.objects.create(name='Cardio Blast', description='Intensywny trening cardio', suggested_for_team=marvel)
        Workout.objects.create(name='Strength Builder', description='Trening siłowy', suggested_for_team=dc)

        # Dodaj leaderboard
        Leaderboard.objects.create(user=users[0], points=100)
        Leaderboard.objects.create(user=users[1], points=90)
        Leaderboard.objects.create(user=users[2], points=110)
        Leaderboard.objects.create(user=users[3], points=95)

        self.stdout.write(self.style.SUCCESS('Baza danych octofit_db została wypełniona przykładowymi danymi.'))
