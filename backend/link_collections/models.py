from django.db import models


class Collection(models.Model):
    name = models.CharField(verbose_name="Название", max_length=50)
    short_description = models.CharField(
        verbose_name="Краткое описание", max_length=100, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="link_collections",
    )

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"

    def __str__(self) -> str:
        return f"Коллекция - {self.name}"
