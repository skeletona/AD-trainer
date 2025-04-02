from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class Game(models.Model):
    start = models.DateTimeField(
        verbose_name="Время начала"
    )
    
    duration = models.PositiveIntegerField(
        verbose_name="Длительность (в минутах)",
        help_text="Например: 540 = 9 часов",
        default=540
    )

    end = models.DateTimeField(
        verbose_name="Время конца"
    )
    
    services = models.JSONField(
        verbose_name="Список сервисов",
        default=list
    )
    
    players = models.JSONField(
        verbose_name="Список игроков",
        default=list
    )

    class Meta:
        db_table = 'games'

    def __str__(self):
        return f"Игра №{self.id}"
    
    def time_left(self):
        return self.start + timezone.timedelta(minutes=self.duration)


class User(AbstractUser):
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, db_column="game")
    first_name = None
    last_name = None
    
    class Meta:
        db_table = 'users'
