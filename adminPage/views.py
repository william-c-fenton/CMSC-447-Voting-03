from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import PollItem
from django.contrib import messages
from datetime import datetime
from pytz import timezone
# Create your views here.


def index(request):
    if request.method == 'POST':

        question = request.POST['addingQuestion']
        option1 = request.POST['addingQuestionOption1']
        option2 = request.POST['addingQuestionOption2']
        option3 = request.POST['addingQuestionOption3']
        option4 = request.POST['addingQuestionOption4']
        print(question,option1,option2,option3,option4)
        error = "No error"
        tz = timezone('EST')
        now = datetime.now(tz).time()
        morning = now.replace(hour=8, minute=0, second=0, microsecond=0)
        closing = now.replace(hour=16, minute=0, second=0, microsecond=0)
        if question and option1 and morning < now > closing:
            pollitem = PollItem()
            pollitem.question = question
            pollitem.option1 = option1
            pollitem.option2 = option2
            pollitem.option3 = option3
            pollitem.option4 = option4
            pollitem.save()
        else:
            if not question or not option1:
                error = PrintError(request, 1)
            elif morning < now > closing:
                error = PrintError(request, 2)
    data = PollItem.objects.all()
    return render(request, 'adminPage/index.html', {"pollItems": data})


def deleteSelectedQuestions(request, question):
    obj = PollItem.objects.filter(question=question)
    obj.delete()
    data = PollItem.objects.all()
    return redirect('/login/adminPage')

def PrintError(request, number):
    if number == 1:
        print("Need a question and at least one valid option.")
        messages.success(request, 'Need a question and at least one valid option.')
        return "Need a question and at least one valid option."
    if number == 2:
        print("Need to add questions between 4pm and 8am EST")
        messages.success(request, 'Need to add questions between 4pm and 8am EST')
        return "Need to add questions between 4pm and 8am EST"
