from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.urls import re_path
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('play', views.play, name='play'),
    path('game', views.game, name='game'),
    path('game_results', views.game_results, name='game_results'),
    path('end_game', views.end_game, name='end_game'),
    path('vpn', views.vpn, name='vpn'),
    path('zip', views.zip, name='zip'),
    path('board', views.board, name='board'),
    path('guides', views.guides, name='guides'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.Logout.as_view(next_page='home'), name='logout'),
    re_path(r'^favicon\.ico$', serve, {'path': 'favicon.ico', 'document_root': settings.BASE_DIR}),
]