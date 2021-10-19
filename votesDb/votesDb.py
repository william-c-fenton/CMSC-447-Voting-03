from django.db import models

class Votes(models.Model):
    VOTES = (
        ('Y', 'YES'),
        ('N', 'NO')
    )

    voter = models.CharField(max_length=30)
    selection = models.CharField(max_length=1, choices=VOTES)
    