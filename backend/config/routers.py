from rest_framework.routers import DefaultRouter

from links.viewsets import LinkViewSet

router = DefaultRouter()

router.register("links", LinkViewSet, basename="links")
