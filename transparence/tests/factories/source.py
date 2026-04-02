import factory
from faker import Faker

from transparence.models import Source
from transparence.tests.factories.legal_case import LegalCaseFactory

fake = Faker()


class SourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Source

    external_id = factory.Faker("uuid4")
    url = factory.Faker("url")
    title = factory.Faker("bs")
    publisher = factory.Faker("company")
    description = factory.Faker("catch_phrase")
    type = "PRESSE"

    published_at = factory.Faker("date")

    legal_case = factory.SubFactory(LegalCaseFactory)
