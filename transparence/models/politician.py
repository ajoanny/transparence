from django.db import models


class Politician(models.Model):
    external_id = models.CharField(max_length=100, unique=True)

    full_name = models.CharField(max_length=250)
