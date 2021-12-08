from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.debug import sensitive_variables
from hashlib import sha256

from .models import Choice, Question, Vote
from loginPage.models import VoterInfo
from django.views.generic.edit import CreateView
from polls.forms import QuestionForm, ChoiceForm

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# !!! EDITED !!!
def voteSuccessful(request):
    return render(request, 'polls/voteSuccessful.html', context={})

@sensitive_variables('voter_info', 'voter_idnum', 'hash_func', 'hashed_idnum')
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question)
    votes = []
    for achoice in choices:
        choice_votes = Vote.objects.filter(choice=achoice)
        for avote in choice_votes:
            votes.append(avote)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    # Add new vote object stored in list of vote objects for each choice
    # Number of vote objects in the list for each choice is the number of votes received
    else:
        # Associate a user's vote with their voterinfo
        if request.user.is_authenticated:
            voter_info = VoterInfo.objects.get(email=request.user.email)
            voter_idnum = voter_info.IDNum
            
            hash_func = sha256()
            hash_func.update(voter_idnum.encode())
            hashed_idnum = hash_func.digest()

            voted = False
            # Iterate through the votes for a ballot to see if user has already voted
            for avote in votes:
                if avote.voter == f'{hashed_idnum}':
                    voted = True

            # Return an error if the user has already voted before
            if voted:
                return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "You have already voted on this ballot.",
                })
            else:
                selected_choice.vote_set.create(choice=selected_choice, voter=f'{hashed_idnum}')
                return HttpResponseRedirect(reverse('polls:voteSuccessful'))

# Method for question creation page at polls/CreateQuestion
# Redirects user to choice creation page after successful question creation
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            new_question = form.save()

            return HttpResponseRedirect(reverse('polls:create-choice', args=(new_question.id,)))

    else:
        form = QuestionForm()

    return render(request, 'polls/question_form.html', {'form': form})


# Method for question creation page at polls/CreateQuestion
# Redirects user to choice creation page after successful question creation
def create_choice(request, pk):
    form = ChoiceForm()

    if request.method == 'POST':

        # Save new choice if save button was pressed
        if "savebtn" in request.POST:
            form = ChoiceForm(request.POST)

            # make sure that choice text is valid and not empty
            if form.is_valid() and form.cleaned_data['choice_text'] != '':
                q = Question.objects.get(pk=pk)
                q.choice_set.create(choice_text=form.cleaned_data['choice_text'])
                return HttpResponseRedirect(reverse('polls:create-choice', args=(pk,)))
        else:
            return HttpResponseRedirect(reverse('polls:detail', args=(pk,)))

    return render(request, 'polls/choice_form.html', {'form': form})
