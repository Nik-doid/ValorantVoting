from django.urls import path
from . import views

urlpatterns = [
    path('', views.player_list, name='player_list'),
    path('vote/<int:player_id>/', views.vote_player, name='vote_player'),
]