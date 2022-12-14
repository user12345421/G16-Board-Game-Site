from django import forms

from .models import Boardgame, Lending

#Form for boardgames
class BoardgameForm(forms.ModelForm):

    class Meta:
        model = Boardgame
        fields = ['name', "genres", "summary",]

#Form for lending
class LendingForm(forms.ModelForm):

    #def save(self, *args, **kwargs):
    #   super().save(*args, **kwargs)  # Call the "real" save() method.

    class Meta:
        model = Lending
        
        fields = ['return_date',]