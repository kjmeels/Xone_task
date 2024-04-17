from datetime import datetime

import factory
from factory import fuzzy

from links.constants import LinkChoices
from links.models import Link
from users.tests.factories import UserFactory


class LinkFactory(factory.django.DjangoModelFactory):
    header = factory.Faker("word")
    description = factory.Faker("sentence")
    link = factory.Sequence(lambda x: f"http://example.com/{x}")
    image = factory.django.ImageField(filename="test.png")
    link_type = fuzzy.FuzzyChoice(choices=LinkChoices.values)
    created_at = datetime.now()
    updated_at = datetime.now()
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Link
