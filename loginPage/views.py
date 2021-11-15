from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from loginPage.models import VoterInfo
from django.urls import reverse
# Create your views here.

# The webpage will load here by default, then redirect to login page
def index(request):
    return HttpResponseRedirect(reverse('login'))

# The main login page without error message
def login(request):
    voterinfo = VoterInfo.objects.filter()
    context = {
        'voterinfo': voterinfo,
    }
    return render(request, 'loginPage/login.html', context=context)

# The main login page with error, shown when user enters incorrect info
def loginError(request):
    voterinfo = VoterInfo.objects.filter()
    context = {
        'voterinfo': voterinfo,
    }
    return render(request, 'loginPage/loginError.html', context=context)

# Page when user successfully logs in. Temporary page to use before voting page is made.
def loginSuccess(request):
    return render(request, 'loginPage/loginSuccess.html', context={})

# Checks user input, then redirects to proper webpage.
def checkLogin(request):
    # -This code was run to add a user into the database-
    
    # Before attempting to log into the website, you must have a user in your database.
    # To add one, follow these instructions:
    #   1. In terminal, type 'python manage.py shell'
    #   2. Type p = VoterInfo(firstName='John', lastName='smith', ..., email='test@example.com')
    #       Make sure you fill in all the fields! Check models.py for fields available. 
    #   3. Type p.save()
    #   Now you should have a user in your database to log in with. 

    voter_first_name = request.POST.get('first name')
    voter_last_name = request.POST.get('last name')
    voter_state = request.POST.get('state')
    voter_idnum = request.POST.get('IDNum')
    voter_email = request.POST.get('email')

    voterinfo = VoterInfo.objects.filter(
        firstName__iexact=voter_first_name,
        lastName__iexact=voter_last_name,
        state__iexact=voter_state,
        IDNum__exact=voter_idnum,
        email__iexact=voter_email
    )

    if voterinfo:
        return HttpResponseRedirect(reverse('loginSuccess'))

    return HttpResponseRedirect(reverse('loginError'))

# An attempt was made to use parameters for path(), but was unsuccessful.
# These are code bits that may be used for the implementation later
# return HttpResponseRedirect(reverse('login', kwargs={'valid': True}))
