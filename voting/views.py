from django.shortcuts import render, redirect
from .models import Player
from django.http import HttpResponse
import random

def home_page(request):
    players = Player.objects.all().order_by('-votes')  # Sort by highest votes
    return render(request, 'home_page.html', {'players': players})

def voting_page(request):
    if 'current_player' not in request.session:
        request.session['current_player'] = None

    if 'remaining_players' not in request.session:
        request.session['remaining_players'] = list(Player.objects.values_list('id', flat=True))
        random.shuffle(request.session['remaining_players'])

    # If no players are left, reset and redirect
    if not request.session['remaining_players']:
        request.session['current_player'] = None
        return redirect('home_page')

    # Set the current player to the winner if available
    if request.session['current_player'] is None:
        request.session['current_player'] = request.session['remaining_players'].pop()

    current_player = Player.objects.get(id=request.session['current_player'])
    challenger_id = request.session['remaining_players'].pop()
    challenger = Player.objects.get(id=challenger_id)

    request.session['challenger'] = challenger.id
    request.session.modified = True

    return render(request, 'voting_page.html', {
        'current_player': current_player,
        'challenger': challenger,
    })

def vote_player(request, winner_id, loser_id):
    winner = Player.objects.get(id=winner_id)
    loser = Player.objects.get(id=loser_id)

    # Increment vote count for the winner
    winner.votes += 1
    winner.save()

    # Set the winner as the current player
    request.session['current_player'] = winner.id

    return redirect('voting_page')