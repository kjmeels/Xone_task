from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from common.permissions import IsOwner
from links.models import Link
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
        if self.action in ["list", "delete_link"]:
            return Collection.objects.filter(user=self.request.user).prefetch_related("links")
        return Collection.objects.filter(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="link_id", description="Id ссылки", required=True, type=OpenApiTypes.INT
            )
        ]
    )
    @action(detail=True, methods=["POST"])
    def add_link(self, request, *args, **kwargs) -> Response:
        link_id = request.query_params.get("link_id")
        if link_id:
            instance = self.get_object()
            link = Link.objects.get(id=link_id)
            if link not in instance.links.all():
                instance.links.add(link)
                return Response(
                    {"collection_id": instance.id, "link_id": link_id},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"link_id": "уже была добавлена в коллекцию"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"link_id": "обязательный параметр"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="link_id", description="Id ссылки", required=True, type=OpenApiTypes.INT
            )
        ]
    )
    @action(detail=True, methods=["DELETE"])
    def delete_link(self, request, *args, **kwargs) -> Response:
        link_id = request.query_params.get("link_id")
        if link_id:
            instance = self.get_object()
            instance_links_ids = [link.id for link in instance.links.all()]
            if int(link_id) in instance_links_ids:
                instance.links.remove(link_id)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"link_id": "уже была удалена из коллекции"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"link_id": "обязательный параметр"}, status=status.HTTP_400_BAD_REQUEST)
