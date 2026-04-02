from django.db import models

from transparence.models.legal_case import LegalCase


class Source(models.Model):
    external_id = models.CharField(max_length=100)
    url = models.URLField(max_length=1000, null=True, blank=True)
    publisher = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    title = models.TextField()
    description = models.TextField()

    published_at = models.DateField()

    legal_case = models.ForeignKey(
        LegalCase, on_delete=models.CASCADE, related_name="sources"
    )
