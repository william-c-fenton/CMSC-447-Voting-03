from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


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
        ).order_by('-pub_date')[:5]


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

@sensitive_variables('voter_info')
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
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
            selected_choice.vote_set.create(choice=selected_choice, voter=voter_info)

            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


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