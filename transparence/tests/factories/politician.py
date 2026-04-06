import factory
from faker import Faker

from transparence.models import Politician

fake = Faker()


class PoliticianFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Politician

    external_id = factory.Faker("uuid4")
    full_name = factory.Faker("name")
