from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy


def home(request):
    return render(request, "home.html")

def play(request):
    return render(request, "play.html")

def guides(request):
    return render(request, "guides.html")

def game(request):
    return render(request, "game.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'error': 'Неверный логин или пароль.'})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class Logout(LogoutView):
    next_page = reverse_lazy('home')

