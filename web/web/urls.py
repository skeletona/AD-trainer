from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('play', views.play, name='play'),
    path('game', views.game, name='game'),
    path('vpn', views.vpn, name='vpn'),
    path('zip', views.zip, name='zip'),
    path('board', views.board, name='board'),
    path('guides', views.guides, name='guides'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.Logout.as_view(next_page='home'), name='logout'),
]

urlpatterns += staticfiles_urlpatterns()