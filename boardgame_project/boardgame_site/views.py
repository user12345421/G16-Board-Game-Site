from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
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
    #Fetching all lends that havent been returned
    currentLends = Lending.objects.filter(received_game_date__isnull = True)

    #Checking if user is logged in
    if request.user.is_authenticated:
        #Fetching and counting all lends by user that havent been returned
        loanCount = currentLends.filter(lender = request.user).count()
    else:
        loanCount = None


    #Passing all these to html page
    context = {"games": games, "lends": currentLends, "loanCount": loanCount,}
    return render(request, "boardgame_site/games.html", context)


@login_required
def game(request, game_id):
    """"Show a single game"""
    game = Boardgame.objects.get(id=game_id)

    lends = Lending.objects.filter(game = game_id)

    #Fetching and counting all lends by user that havent been returned
    loanCount = Lending.objects.filter(received_game_date__isnull = True, lender = request.user).count()

    context = {"game": game, "lends": lends, "loanCount": loanCount}
    return render(request, "boardgame_site/game.html", context)

@login_required
def new_game(request):
    """Adds a new game"""

    if request.method != "POST":
        #Runs when no data is submitted. Creates a blank form
        form = BoardgameForm
    else:
        #Making a boardgame object. And setting the owner to be the user
        gameObj = Boardgame(owner = request.user)
        form = BoardgameForm(data = request.POST, instance = gameObj)
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

    #Fetching all lends that havent been returned yet
    currentLends = Lending.objects.filter(received_game_date__isnull = True)

    #Fetch all unreturned lends that are lent by the user
    userLends = currentLends.filter(lender = request.user)

    #Checking users lend count
    userLendCount = userLends.count()

    #Check if the game is already lent and not returned

    if currentLends.filter(game=gameObj):

        return redirect("boardgame_site:message")


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

    #Checking if user is logged in
    if request.user.is_authenticated:
        #Fetching all lends by user that havent been returned
        owned = Lending.objects.filter(lender = request.user, received_game_date__isnull = True)
    else:
        owned = None
    

    #All lends sorted by return_date
    returnedLends = Lending.objects.filter(received_game_date__isnull = False)
    lends = Lending.objects.filter(received_game_date__isnull = True).order_by("return_date")

    #Passing the lends
    context = {"lends": lends, "ownLends": owned, "returnedLends": returnedLends}
    return render(request, "boardgame_site/lendings.html", context)

@login_required
def return_game(request, lend_id):
    """Return a lent boardgame"""

    #The lend obj
    lend = Lending.objects.get(id=lend_id)

    #Checking if the lend is made by the user
    if lend.lender != request.user:
        raise Http404
    #Sets the return date to today. Making the lend completed.
    if request.method != "POST":
        
        lend.received_game_date = datetime.now()

        #Save the changes
        lend.save()
        return redirect("boardgame_site:lendings")

def message(request):
    return render(request, "boardgame_site/message.html")