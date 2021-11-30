from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import PollItem

# Create your views here.


def index(request):
    if request.method == 'POST':
        question = request.POST['addingQuestion']
        option1 = request.POST['addingQuestionOption1']
        option2 = request.POST['addingQuestionOption2']
        option3 = request.POST['addingQuestionOption3']
        option4 = request.POST['addingQuestionOption4']
        print(question,option1,option2,option3,option4)
        pollitem = PollItem()
        pollitem.question = question
        pollitem.option1 = option1
        pollitem.option2 = option2
        pollitem.option3 = option3
        pollitem.option4 = option4
        pollitem.save()
    data = PollItem.objects.all()
    print(data)
    return render(request, 'adminPage/index.html', {"pollItems": data})


def deleteSelectedQuestions(request):
    print("deleteing questions")
    data = PollItem.objects.all()
    return HttpResponseRedirect('/adminPage')

