from django.db import models

class Politician(models.Model):
    external_id = models.CharField(max_length=100)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    civility = models.CharField(max_length=100)
