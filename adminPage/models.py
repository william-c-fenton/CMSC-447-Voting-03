from django.db import models

# Create your models here.

'''
class PollList(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
'''

class PollItem(models.Model):
    #pollList = models.ForeignKey(PollList, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    def __str__(self):
        return self.question
