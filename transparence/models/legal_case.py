from django.db import models

from transparence.models import Politician
from transparence.models.party import Party


class LegalCase(models.Model):
    external_id = models.CharField(max_length=100, db_index=True)
    external_updated_at = models.DateTimeField(null=True, blank=True)

    category = models.CharField(max_length=100, db_index=True)
    title = models.TextField()
    description = models.TextField()

    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100)
    verdict_date = models.DateField(null=True, blank=True)

    party = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        related_name="legal_cases",
    )

    politician = models.ForeignKey(
        Politician, on_delete=models.CASCADE, related_name="legal_cases"
    )
