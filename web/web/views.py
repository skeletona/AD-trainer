from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.urls import reverse_lazy
import os

def home(request):
    return render(request, "home.html")

@login_required
def play(request):
    if request.user.game is not None:
        return redirect('game')
    else:
        return render(request, "play.html")

@login_required
def guides(request):
    return render(request, "guides.html")

@login_required
def game(request):
    return render(request, "game.html")

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect(request.GET.get("next", "home"))
        return render(request, 'login.html', {'error': 'Wrong username or password'})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def vpn(request):
    os.system('docker exec -d vpn ./genclient.sh')
    config = os.popen('docker exec vpn sh -c "./getconfig.sh \$(ls /opt/Dockovpn_data/clients/ -t | head -1)"').read()
    response = HttpResponse(config, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="game.ovpn"'
    return response

class Logout(LogoutView):
    next_page = reverse_lazy('home')