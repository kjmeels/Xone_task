import factory
from factory.django import DjangoModelFactory

from ..models import User


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda x: f"user_{x}")

    class Meta:
        model = User


