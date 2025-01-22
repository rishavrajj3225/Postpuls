from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User  
from django.contrib.auth.decorators import login_required  

def home(request):
    return render(request, 'home.html')


@login_required
def user_account(request):
    # Get the current logged-in user's profile information
    user = request.user
    return render(request, 'user_account.html', {'user': user})