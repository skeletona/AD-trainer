from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('play', views.play, name='play'),
    path('game', views.game, name='game'),
    path('guides', views.guides, name='guides'),
    path('register', views.CustomRegisterView.as_view(), name='register'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', views.CustomLogoutView.as_view(), name='logout'),
]

urlpatterns += staticfiles_urlpatterns()