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
def checkInput(request):
    # -This code was run to add a user into the database-
    # VoterInfo.objects.filter(IDNum='12345').delete()
    # info = VoterInfo(firstName="Test", lastName="Guy", state="Maryland", IDNum="12345", email="123@email.com",)
    # info.save()
    voterinfo = VoterInfo.objects.filter()

    for info in voterinfo:
        if info.firstName == request.POST.get("first name"):
            if info.lastName == request.POST.get("last name"):
                if info.state == request.POST.get("state"):
                    if info.IDNum == request.POST.get("IDNum"):
                        if info.email == request.POST.get("email"):
                            return HttpResponseRedirect(reverse('loginSuccess'))

    return HttpResponseRedirect(reverse('loginError'))

# An attempt was made to use parameters for path(), but was unsuccessful.
# These are code bits that may be used for the implementation later
# return HttpResponseRedirect(reverse('login', kwargs={'valid': True}))
