from django.db import models

class Party(models.Model):
    abbreviation = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, unique=True)