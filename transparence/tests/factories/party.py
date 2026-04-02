import factory
from faker import Faker

from transparence.models import Party

fake = Faker()


class PartyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Party

    abbreviation = factory.Sequence(lambda n: f"ABR-{n}")
    name = factory.Faker("company")
