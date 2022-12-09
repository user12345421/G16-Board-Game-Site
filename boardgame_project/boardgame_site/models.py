from django.db import models
#Importing the default User class from django.auth
from django.contrib.auth.models import User


#Lending class
class Lending(models.Model):
    #the lender user
    lender = models.ForeignKey(User, on_delete=models.CASCADE)
    #Lend starting date
    lend_start_date = models.DateTimeField(auto_now_add=True)
    #Return date for the game
    return_date = models.DateTimeField()

    #def __str__(self):
    #    """Return the name of the lent game"""
    #    return self.boardgame_set.name

#The boardgame classs
class Boardgame(models.Model):
    """A boardgame"""
    #Name of the game
    name = models.CharField(max_length=200)
    #Genres of the game
    genres = models.CharField(max_length=400)
    #A brief summery of the game
    summary = models.CharField(max_length=500)
    #Lending object
    lending_obj = models.ManyToManyField(Lending)
    #Bool to check if game is avaible for lending
    available_to_lend = models.BooleanField()
    #Owner of the game
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #Dates
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the name of the game"""
        return self.name

