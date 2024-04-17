from rest_framework import serializers

from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    """Сериализатор ссылок."""

    class Meta:
        model = Link
        fields = (
            "id",
            "link",
        )


class LinkDetailSerializer(serializers.ModelSerializer):
    """Сериализатор деталки ссылки."""

    class Meta:
        model = Link
        fields = (
            "id",
            "header",
            "description",
            "link",
            "image",
            "link_type",
            "created_at",
            "updated_at",
        )


class LinkCreateSerializer(serializers.ModelSerializer):
    """Сериализатор на создание ссылок."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Link
        fields = (
            "link",
            "user",
        )


class LinkUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор на обновление ссылок."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Link
        fields = (
            "header",
            "description",
            "image",
            "link_type",
            "user",
        )
