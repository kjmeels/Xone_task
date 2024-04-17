from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .models import Link
from common.permissions import IsOwner
from .serializers import (
    LinkSerializer,
    LinkDetailSerializer,
    LinkCreateSerializer,
    LinkUpdateSerializer,
)

from bs4 import BeautifulSoup
import requests


@extend_schema(tags=["Links"])
class LinkViewSet(ModelViewSet):
    """Вьюсет ссылок."""

    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self) -> type[ModelSerializer]:
        if self.action == "list":
            return LinkSerializer
        if self.action == "retrieve":
            return LinkDetailSerializer
        if self.action == "create":
            return LinkCreateSerializer
        if self.action == "update":
            return LinkUpdateSerializer

    def get_queryset(self) -> QuerySet:
        return Link.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        extract_data = self._extract_data_from_page(obj.link)
        if extract_data:
            obj.header = extract_data.get("title", "")
            obj.description = extract_data.get("description", "")
            obj.image = extract_data.get("image", None)
            obj.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def _extract_data_from_page(url: str) -> dict[str, str] | None:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser", from_encoding="utf-8")

            og_data: dict[str, str] = {}
            og_tags = (
                soup.find_all("meta", attrs={"property": "og:title"})
                + soup.find_all("meta", attrs={"property": "og:description"})
                + soup.find_all("meta", attrs={"property": "og:image"})
            )
            for tag in og_tags:
                og_data[tag["property"][3:]] = tag["content"]

            if og_data:
                return og_data

            title: str = soup.find("title").get_text() if soup.find("title") else ""
            meta_desc: str = (
                soup.find("meta", {"name": "description"})["content"]
                if soup.find("meta", {"name": "description"})
                else ""
            )

            return {"title": title, "description": meta_desc}

        else:
            return None
