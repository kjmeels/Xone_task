from copy import deepcopy

from django.contrib.auth import authenticate, login
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import (
    UserCreateSerializer,
    UserChangePasswordSerializer,
    UserLoginSerializer,
)


@extend_schema(tags=["User"])
class UserViewSet(GenericViewSet):
    """Вьюсет пользователя."""

    def get_serializer_class(self) -> type[BaseSerializer] | None:
        if self.action == "create":
            return UserCreateSerializer
        if self.action == "change_password":
            return UserChangePasswordSerializer
        if self.action == "login":
            return UserLoginSerializer

    def get_queryset(self) -> QuerySet:
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User(email=serializer.validated_data["email"])
        user.set_password(raw_password=serializer.validated_data["password"])
        user.save()
        serializer_data = deepcopy(serializer.data)
        serializer_data["password"] = user.password
        return Response(serializer_data, status=status.HTTP_201_CREATED)

    @extend_schema(request=UserChangePasswordSerializer, responses=None)
    @action(detail=False, methods=["POST"])
    def change_password(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.check_password(raw_password=serializer.validated_data["old_password"]):
            user.set_password(raw_password=serializer.validated_data["new_password"])
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"old_password": "неверно введен пароль"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["POST"])
    def reset_password(self, request, *args, **kwargs) -> Response:
        user = self.request.user
        if user.is_authenticated:
            user.set_password(raw_password="1111")
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(request=UserLoginSerializer, responses=None)
    @action(detail=False, methods=["POST"])
    def login(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if user is not None:
            login(request, user)
            return Response({"status": "авторизирован"}, status=status.HTTP_200_OK)
        return Response({"status": "неверные почта или пароль"}, status=status.HTTP_400_BAD_REQUEST)
