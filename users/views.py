from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        #Display blank regestration form.
        form = UserCreationForm()
    else:
        # process completed form.
        form = UserCreationForm(data=request.POST)
    # username has the appropiate characters, the passwords match,
    # and the user isn't trying to do anything malicious in thier submission.
        if form.is_valid():
        # The save() method returns the newly created user object,
        # which we assign to a new user.
            new_user = form.save()
        # Log the user in and then redirect them to homepage.
            login(request,new_user)
            return redirect('MainApp:index')
    context = {'form':form}
    return render(request,'registration/register.html', context)