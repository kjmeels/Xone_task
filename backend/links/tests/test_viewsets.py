from functools import partial

from django.db import IntegrityError
from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase

from common.utils import generate_image_file
from links.constants import LinkChoices
from links.models import Link
from links.tests.factories import LinkFactory
from users.tests.factories import UserFactory


@mark.django_db
class TestLinkViewSet(APITestCase):
    def setUp(self):
        self.list_url: str = reverse("links-list")
        self.retrieve_url = partial(reverse, "links-detail")

    def test_list(self):
        users = [UserFactory() for _ in range(5)]
        links = [LinkFactory(user=user) for user in users for _ in range(10)]

        self.client.force_authenticate(user=users[0])

        with self.assertNumQueries(1):
            res = self.client.get(self.list_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json), len(links) // len(users))

    def test_create(self):
        user = UserFactory()
        payload = {"link": "http://example.com"}

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.post(self.list_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Link.objects.count(), 1)

        try:
            with self.assertNumQueries(2):
                res = self.client.post(self.list_url, data=payload)
        except IntegrityError:
            pass
        except Exception:
            self.fail("Не отработал UniqueConstraint")
        else:
            self.fail("Не отработал UniqueConstraint")

    def test_update(self):
        user = UserFactory()
        link = LinkFactory(user=user, image=None)
        payload = {
            "header": "New header",
            "description": "Updated description",
            "image": generate_image_file(),
            "link_type": LinkChoices.ARTICLE,
        }

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(3):
            res = self.client.put(self.retrieve_url(kwargs={"pk": link.id}), data=payload)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Link.objects.count(), 1)
        link.refresh_from_db()
        link_obj = Link.objects.first()
        self.assertEqual(link_obj.header, payload["header"])
        self.assertEqual(link_obj.description, payload["description"])
        self.assertTrue(link_obj.image)
        self.assertEqual(link_obj.link_type, payload["link_type"])

    def test_destroy(self):
        user = UserFactory()
        link = LinkFactory(user=user)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(4):
            res = self.client.delete(self.retrieve_url(kwargs={"pk": link.id}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Link.objects.count(), 0)

    def test_retrieve(self):
        user = UserFactory()
        link = LinkFactory(user=user)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.get(self.retrieve_url(kwargs={"pk": link.pk}))

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json["id"], link.pk)
