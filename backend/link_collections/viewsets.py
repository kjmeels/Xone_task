from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from common.permissions import IsOwner
from .models import Collection
from .serializers import (
    CollectionSerializer,
    CollectionDetailSerializer,
    CollectionCreateUpdateSerializer,
)


@extend_schema(tags=["collections"])
class CollectionViewSet(ModelViewSet):
    """Вьюсет коллекций."""

    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self) -> type[ModelSerializer]:
        if self.action == "list":
            return CollectionSerializer
        if self.action == "retrieve":
            return CollectionDetailSerializer
        if self.action in ["create", "update"]:
            return CollectionCreateUpdateSerializer

    def get_queryset(self) -> QuerySet:
        return Collection.objects.filter(user=self.request.user)
