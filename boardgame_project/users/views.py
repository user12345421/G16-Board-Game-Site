from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


#Register view
def register(request):
    """Register a new user"""

    if request.method != "POST":
        #Display a blank registraion form
        form = UserCreationForm()
    else:
        #Processs completed form
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Log the user in annd redirect to home page
            login(request, new_user)
            return redirect("boardgame_site:index")

    context = {"form": form}
    return render(request, "registration/register.html", context)