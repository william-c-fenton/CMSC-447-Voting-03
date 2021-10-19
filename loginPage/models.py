from django.db import models

# Create your models here.

# An object to keep track of user identification (not implemented yet)
class VoterInfo(models.Model):
    firstName = models.TextField()
    lastName  = models.TextField()
    state     = models.TextField()