from django.contrib.auth.models import AbstractUser
from django.db import models


class Game(models.Model):
    start = models.DateTimeField(
        verbose_name="Время начала",
        auto_now_add=False,
        default="2024-01-01T00:00:00"
    )
    
    duration = models.PositiveIntegerField(
        verbose_name="Длительность (в минутах)",
        help_text="Например: 540 = 9 часов",
        default=540
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


class User(AbstractUser):
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, db_column="game")
    first_name = None
    last_name = None
    
    class Meta:
        db_table = 'users'
