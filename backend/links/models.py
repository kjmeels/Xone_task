from django.db import models

from links.constants import LinkChoices


class Link(models.Model):
    header = models.TextField(verbose_name="Заголовок страницы", default="", blank=True)
    description = models.TextField(verbose_name="Краткое описание", default="", blank=True)
    link = models.URLField(verbose_name="Ссылка на страницу")
    image = models.ImageField(verbose_name="Картинка", upload_to="l/l/i", null=True, blank=True)
    link_type = models.CharField(
        verbose_name="Тип ссылки",
        max_length=50,
        choices=LinkChoices.choices,
        default=LinkChoices.WEBSITE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Пользователь", related_name="links"
    )
    collections = models.ManyToManyField(
        "link_collections.Collection", verbose_name="Коллекция", related_name="links"
    )

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"
        constraints = [
            models.UniqueConstraint(fields=["link", "user"], name="unique_user_link"),
        ]

    def __str__(self) -> str:
        return f"Ссылка - {self.link}"
