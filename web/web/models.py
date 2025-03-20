from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username',)  # Только логин и пароль
