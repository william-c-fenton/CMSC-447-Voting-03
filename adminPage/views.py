from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'adminPage/index.html', context={})


def information(request):
    return render(request, 'adminPage/information.html', context={})


def polls(request):
    return render(request, 'adminPage/polls.html', context={})
