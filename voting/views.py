from django.shortcuts import render, redirect
from .models import Player
from django.http import HttpResponse

def player_list(request):
    players = Player.objects.all().order_by('name')
    return render(request, 'player_list.html', {'players': players})

def vote_player(request, player_id):
    
    voted_players = request.COOKIES.get('voted_players', '')

    if str(player_id) in voted_players.split(','):
        return HttpResponse("You have already voted for this player!")

   
    player = Player.objects.get(id=player_id)
    player.votes += 1
    player.save()

   
    response = redirect('player_list')

   
    new_voted_players = f"{voted_players},{player_id}" if voted_players else str(player_id)
    response.set_cookie('voted_players', new_voted_players, max_age=7 * 24 * 60 * 60)  
    return response
