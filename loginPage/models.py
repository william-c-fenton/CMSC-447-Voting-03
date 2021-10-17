from django.db import models

# Create your models here.
class VoterInfo(models.Model):
    firstName = models.TextField()
    lastName  = models.TextField()
    state     = models.TextField()