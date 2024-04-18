from rest_framework.routers import DefaultRouter

from link_collections.viewsets import CollectionViewSet
from links.viewsets import LinkViewSet

router = DefaultRouter()

router.register("links", LinkViewSet, basename="links")
router.register("link_collections", CollectionViewSet, basename="link_collections")
