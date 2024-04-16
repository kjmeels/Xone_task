from rest_framework import serializers

from .models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            "id",
            "name",
        )


class CollectionDetailSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Collection
        fields = (
            "name",
            "short_description",
        )
