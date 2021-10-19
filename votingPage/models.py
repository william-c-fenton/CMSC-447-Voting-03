from django.db import models
from ./loginPage import models.py

# Create your models here.
class Ballot(models.Model):
    option = models.CharField(max_length=50)

class Votes(models.Model):
    voter = models.ForeignKey(VoterInfo, on_delete=models.CASCADE)
    vote = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    