from django.shortcuts import render, redirect, reverse
from web.models import CustomUserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.urls import reverse_lazy
import subprocess

def home(request):
    return render(request, "home.html")

def play(request):
    return render(request, "play.html")

def guides(request):
    return render(request, "guides.html")

def game(request):
    return render(request, "game.html")

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

