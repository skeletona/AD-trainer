from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


User = get_user_model()

class LoginForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise ValidationError(
                    self.error_messages['invalid_username'],
                    code='invalid_username',
                )
            
            if not user.check_password(password):
                raise ValidationError(
                    self.error_messages['invalid_password'],
                    code='invalid_password',
                )

            # Стандартная проверка аутентификации
            self.confirm_login_allowed(user)

        return self.cleaned_data

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
        default=list  # По умолчанию пустой список
    )
    
    players = models.JSONField(
        verbose_name="Список игроков",
        default=list
    )

    class Meta:
        db_table = 'games'  # Явное имя таблицы в БД
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['-start']

    def __str__(self):
        return f"Игра от {self.start}"