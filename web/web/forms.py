from django.db import models
from django.contrib.auth.forms import UserCreationForm
from core.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', )


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
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['-start']

    def __str__(self):
        return f"Игра от {self.start}"
