from rest_framework import serializers

from .models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    """Сериализатор коллекций."""

    class Meta:
        model = Collection
        fields = (
            "id",
            "name",
        )


class CollectionDetailSerializer(serializers.ModelSerializer):
    """Сериализатор деталки коллекций."""

    class Meta:
        model = Collection
        fields = (
            "id",
            "name",
            "short_description",
            "created_at",
            "updated_at",
            "links",
        )


class CollectionCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор на создание/обновление коллекций."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Collection
        fields = (
            "name",
            "short_description",
            "user",
        )
