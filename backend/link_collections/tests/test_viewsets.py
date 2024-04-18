from functools import partial

from django.db import IntegrityError
from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase

from link_collections.models import Collection
from link_collections.tests.factories import CollectionFactory
from users.tests.factories import UserFactory


@mark.django_db
class TestLinkViewSet(APITestCase):
    def setUp(self):
        self.list_url: str = reverse("link_collections-list")
        self.retrieve_url = partial(reverse, "link_collections-detail")

    def test_list(self):
        users = [UserFactory() for _ in range(2)]
        collections = [CollectionFactory(user=user) for user in users for _ in range(4)]

        self.client.force_authenticate(user=users[0])

        with self.assertNumQueries(1):
            res = self.client.get(self.list_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json), len(collections) // len(users))

    def test_retrieve(self):
        user = UserFactory()
        collection = CollectionFactory(user=user)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(3):
            res = self.client.get(self.retrieve_url(kwargs={"pk": collection.pk}))

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json["id"], collection.pk)

    def test_destroy(self):
        user = UserFactory()
        collection = CollectionFactory(user=user)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(4):
            res = self.client.delete(self.retrieve_url(kwargs={"pk": collection.id}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collection.objects.count(), 0)

    def test_create(self):
        user = UserFactory()
        payload = {"name": "new name", "short_description": "new description"}

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(1):
            res = self.client.post(self.list_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collection.objects.count(), 1)

    def test_update(self):
        user = UserFactory()
        collection = CollectionFactory(user=user)
        payload = {"name": "new name", "short_description": "new description"}

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(3):
            res = self.client.put(self.retrieve_url(kwargs={"pk": collection.id}), data=payload)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Collection.objects.count(), 1)
        collection.refresh_from_db()
        coll_obj = Collection.objects.first()
        self.assertEqual(coll_obj.name, payload["name"])
        self.assertEqual(coll_obj.short_description, payload["short_description"])
