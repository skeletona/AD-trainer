from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.urls import reverse_lazy
import os

def home(request):
    return render(request, "home.html")

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
    game = request.user.game
    if game:
        return render(request, "game.html", {'time': game.seconds_left()})
    return redirect('play')

@login_required
def end_game(request):
    user = request.user
    if user.game:
        user.game.end_game()
        user.game = None
        user.save()
        return redirect('game_results')
    return redirect('play')

def game_results(request):
    return render(request, 'game_results.html')

@login_required
def vpn(request):
    os.system('docker exec -d vpn ./genclient.sh')
    config = os.popen('docker exec vpn sh -c "./getconfig.sh \$(ls /opt/Dockovpn_data/clients/ -t | head -1)"').read()
    response = HttpResponse(config, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="game.ovpn"'
    return response

@login_required
def board(request):
    return redirect("http://10.0.0.2")


@login_required
def zip(request):
    zip = open(f'../games/{request.user.game.id}/services.7z', 'rb')
    response = HttpResponse(zip, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="services.7z"'
    return response

class Logout(LogoutView):
    next_page = reverse_lazy('home')
