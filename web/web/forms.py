from django.contrib.auth.forms import UserCreationForm
from core.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )
    
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        help_texts = {'username': None}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
