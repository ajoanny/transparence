from django.db import models

from transparence.models import Politician
from transparence.models.party import Party


class LegalCase(models.Model):
    external_id = models.CharField(max_length=100,db_index=True)

    category = models.CharField(max_length=100,db_index=True)
    title = models.TextField()
    description = models.TextField()

    date = models.DateField()
    status = models.CharField(max_length=100)
    verdict_date= models.DateField()

    party = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        related_name="legal_cases"
    )

    politician = models.ForeignKey(
        Politician,
        on_delete=models.CASCADE,
        related_name="legal_cases")
