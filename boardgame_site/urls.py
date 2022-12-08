"""Defines URL patterns for boardgame_site"""

from django.urls import path

from . import views

app_name = 'boardgame_site'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    #Shows all boardgames
    path('games/', views.games, name='games'),
    #Detail page for a single game
    path('games/<int:game_id>/', views.game, name='game'),
    #Page for creating a new boardgame
    path("new_game/", views.new_game, name="new_game"),
    #Page for editing a boardgame
    path("edit_game/<int:game_id>", views.edit_game, name="edit_game"),
    #Page for deleting a boardgame
    path("delete_game/<int:game_id>", views.delete_game, name="delete_game")
]
