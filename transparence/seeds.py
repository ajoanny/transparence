from transparence.models import Party, Politician, LegalCase, Source
from transparence.tests.factories.legal_case import LegalCaseFactory
from transparence.tests.factories.source import SourceFactory


def run():
    Source.objects.all().delete()
    Politician.objects.all().delete()
    LegalCase.objects.all().delete()
    Party.objects.all().delete()

    SourceFactory.create_batch(3)
    LegalCaseFactory.create_batch(10)

    print("Seeds créés avec succès !")
