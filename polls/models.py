import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse
from loginPage.models import VoterInfo


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.pk})


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text


# Vote model gets stored in list of votes for each choice. Each vote is associated
# with a user so that a user can not vote twice in a ballot. The voter field will consist
# of hashed values of the voter's IDNum, for obfuscation and security.
class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.TextField()

