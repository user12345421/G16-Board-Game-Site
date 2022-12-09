from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Boardgame, Lending
from .forms import BoardgameForm, LendingForm
from django.http import Http404


def index(request):
    """"The home page"""
    return render(request, "boardgame_site/index.html")

#No login needed to see this
def games(request):
    """"See all games in a list"""
    games = Boardgame.objects.order_by("date_added")
    context = {"games": games}
    return render(request, "boardgame_site/games.html", context)

@login_required
def game(request, game_id):
    """"Show a single game"""
    game = Boardgame.objects.get(id=game_id)
    context = {"game": game}
    return render(request, "boardgame_site/game.html", context)

@login_required
def new_game(request):
    """Adds a new game"""

    if request.method != "POST":
        #Runs when no data is submitted. Creates a blank form
        form = BoardgameForm
    else:
        form = BoardgameForm(data = request.POST)
        #If form is valid runs this
        if form.is_valid():
            #Save the form

            form.save()
            return redirect("boardgame_site:games")
    #Runs if blank or invalid form(when created)
    context = {"form": form}
    return render(request, "boardgame_site/new_game.html", context)

@login_required
def edit_game(request, game_id):
    """Edit an existing game"""
    game = Boardgame.objects.get(id=game_id)
    #Checking if the game belongs to the user
    if game.owner != request.user:
        raise Http404
    if request.method != "POST":
        #Initial request. Pre-fills the form with the current edited review
        form = BoardgameForm(instance=game)
    else:
        #POST data submitted. Process data
        form = BoardgameForm(instance=game, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect("boardgame_site:games")

    context = {"game": game, "form": form}
    return render(request, "boardgame_site/edit_game.html", context)

@login_required
def delete_game(request, game_id):
    """Delete an existing game"""
    game = Boardgame.objects.get(id=game_id)
    #Checking if the game belongs to the user
    if game.owner != request.user:
        raise Http404
    #Deletes the game and redirects to games list
    if request.method != "POST":
        game.delete()
        return redirect("boardgame_site:games")

@login_required
def lend_game(request, game_id):
    """Lend a boardgame"""
    gameObj = Boardgame.objects.get(id=game_id)

    if request.method != "POST":
        #Runs when no data is submitted. Creates a blank form
        form = LendingForm
    else:
        #Making a lend with the user and game
        lendObj = Lending(lender = request.user, game = gameObj)
        #Passing it to the form
        form = LendingForm(data = request.POST, instance = lendObj)
        #If form is valid runs this
        if form.is_valid():
            #Save the form
            form.save()
            #Return to games page
            return redirect("boardgame_site:games")

    #Runs if blank or invalid form(when created)
    #Passing the game and form to the html page
    context = {"game": gameObj, "form": form}
    return render(request, "boardgame_site/lend_game.html", context)

#No login needed to see this
def lendings(request):
    """"See all current lends"""
    lends = Lending.objects.order_by("return_date")

    #Passing the lends
    context = {"lends": lends}
    return render(request, "boardgame_site/lendings.html", context)