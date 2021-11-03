from django.db import models

# Create your models here.

# An object to keep track of user identification
class VoterInfo(models.Model):
    firstName = models.TextField()
    lastName  = models.TextField()
    state     = models.TextField()
    IDNum     = models.TextField()
    email     = models.TextField()