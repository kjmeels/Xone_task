from datetime import datetime

import factory

from link_collections.models import Collection
from users.tests.factories import UserFactory


class CollectionFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")
    short_description = factory.Faker("sentence")
    created_at = datetime.now()
    updated_at = datetime.now()
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Collection
