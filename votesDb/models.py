from django.db import models

class Votes(models.Model):
    OPTIONS = (
        ('Y', 'Yes'),
        ('N', 'No')
    )
    options = models.CharField(max_length=1, choices=OPTIONS)

    