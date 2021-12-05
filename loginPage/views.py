from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from loginPage.models import VoterInfo
from django.urls import reverse

# !!! added
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.

# The webpage will load here by default, then redirect to login page
def index(request):
    return HttpResponseRedirect(reverse('login'))

# The main login page without error message
def loginPath(request):
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

# Page if user needs help with information on how to login
def loginHelp(request):
    return render(request, 'loginPage/loginHelp.html', context={})

# Main create user page without error message. 
def createUser(request):
    voterinfo = VoterInfo.objects.filter()
    context = {
        'voterinfo': voterinfo,
    }
    return render(request, 'loginPage/createUser.html', context=context)

# Page to show when user tries to create duplicate account. 
def createUserError(request):
    voterinfo = VoterInfo.objects.filter()
    context= {
        'voterinfo': voterinfo,
    }
    return render(request, 'loginPage/createUserError.html', context=context)

# Checks user input, then redirects to proper webpage.
@sensitive_variables()
def checkLogin(request):
    # Before attempting to log into the website, you must have a user in your database.
    # To add one, follow these instructions:
    #   1. In terminal, type 'python manage.py shell'
    #   2. Type p = VoterInfo(firstName='John', lastName='smith', ..., email='test@example.com')
    #       Make sure you fill in all the fields! Check models.py for fields available. 
    #   3. Type p.save()
    #   Now you should have a user in your database to log in with.
    # Alternatively, add a user with the Create User button from the website.  

    voter_first_name = request.POST.get('first name')
    voter_last_name = request.POST.get('last name')
    voter_idnum = request.POST.get('IDNum')

    voterinfo = VoterInfo.objects.filter(
        firstName__iexact=voter_first_name,
        lastName__iexact=voter_last_name,
        IDNum__exact=voter_idnum
    )

    # If the user exists, authenticate the user then login
    if voterinfo:
        # django User object that matches VoterInfo object must exist in order to login
        user = authenticate(username=voter_first_name, password=voter_idnum)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('polls'))

    return HttpResponseRedirect(reverse('loginError'))


# Checks that the user doesn't already exist in the database, and then adds it. 
@sensitive_variables()
def checkUser(request):
    # Checks the database for given information. If it does not already exist in the database, 
    # it will add it. If it does, it redirects to the failure page. 
    voter_first_name = request.POST.get('first name')
    voter_last_name = request.POST.get('last name')
    voter_state = request.POST.get('state')
    voter_idnum = request.POST.get('IDNum')
    voter_email = request.POST.get('email')

    fields = [voter_first_name, voter_last_name, voter_state, voter_idnum, voter_email]

    for field in fields:
        if field == '':
            return HttpResponseRedirect(reverse('createUserError'))

    voterinfo = VoterInfo.objects.filter(
        firstName__iexact=voter_first_name,
        lastName__iexact=voter_last_name,
        state__iexact=voter_state,
        IDNum__exact=voter_idnum,
        email__iexact=voter_email
    )

    if not voterinfo:
        new_voter = VoterInfo(
            firstName = voter_first_name,
            lastName = voter_last_name,
            state = voter_state,
            IDNum = voter_idnum,
            email = voter_email
        )
        new_voter.save()

        # A user will have a VoterInfo object and a django User object
        user = User.objects.create_user(voter_first_name, voter_email, voter_idnum)
        user.save()

        return HttpResponseRedirect(reverse('login'))

    return HttpResponseRedirect(reverse('createUserError'))
# An attempt was made to use parameters for path(), but was unsuccessful.
# These are code bits that may be used for the implementation later
# return HttpResponseRedirect(reverse('login', kwargs={'valid': True}))
