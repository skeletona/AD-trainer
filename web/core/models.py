from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db import models


class Game(models.Model):
    start = models.DateTimeField()
    duration = models.PositiveIntegerField(default=540)
    end = models.DateTimeField()
    services = models.JSONField(default=list)
    players = models.JSONField(default=list)
    
    class Meta:
        db_table = 'games'

    def __str__(self):
        return f"Game {self.id}"
    
    def seconds_left(self):
        return int((self.end - now()).total_seconds())
    
    def end_game(self):
        self.end = now()
        self.save()


class User(AbstractUser):
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, db_column="game")
    first_name = None
    last_name = None
    
    class Meta:
        db_table = 'users'
