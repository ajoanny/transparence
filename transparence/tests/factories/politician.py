import factory
from faker import Faker

from transparence.models import Politician

fake = Faker()


class PoliticianFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Politician

    external_id = factory.Faker("uuid4")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    civility = factory.Faker("prefix")
