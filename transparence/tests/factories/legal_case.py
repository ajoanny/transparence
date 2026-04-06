from datetime import timezone

import factory
from faker import Faker

from transparence.models import LegalCase
from transparence.tests.factories.party import PartyFactory
from transparence.tests.factories.politician import PoliticianFactory

fake = Faker()


class LegalCaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LegalCase

    external_id = factory.Faker("uuid4")
    external_updated_at = factory.Faker("date_time", tzinfo=timezone.utc)
    category = "ABUS_DE_BIENS_SOCIAUX"
    status = "MISE_EN_EXAMEN"

    title = factory.Faker("bs")
    description = factory.Faker("catch_phrase")

    date = factory.Faker("date")
    verdict_date = factory.Faker("date")

    party = factory.SubFactory(PartyFactory)
    politician = factory.SubFactory(PoliticianFactory)
