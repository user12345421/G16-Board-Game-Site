from django import forms

from .models import Boardgame, Lending

#Form for boardgames
class BoardgameForm(forms.ModelForm):

    class Meta:
        model = Boardgame
        fields = ['name', "genres", "summary", "available_to_lend", "owner"]

#Form for lending
class LendingForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ['lender', "return_date"]