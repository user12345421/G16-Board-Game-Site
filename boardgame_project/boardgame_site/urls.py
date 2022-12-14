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
    path("delete_game/<int:game_id>", views.delete_game, name="delete_game"),
    #Page for seeing all lendings
    path('lendings/', views.lendings, name='lendings'),
    #Page for lending games
    path("lend_game/<int:game_id>", views.lend_game, name="lend_game"),
    #Page for returning lent games
    path("return_game/<int:lend_id>", views.return_game, name="return_game"),
    path("message/", views.message, name="message"),
]
