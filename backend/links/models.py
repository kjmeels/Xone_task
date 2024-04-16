from django.db import models

from links.constants import LinkChoices


class Link(models.Model):
    header = models.CharField(verbose_name="Заголовок страницы", max_length=50)
    description = models.CharField(verbose_name="Краткое описание", max_length=100)
    link = models.URLField(verbose_name="Ссылка на страницу")
    image = models.ImageField(verbose_name="Картинка", upload_to="l/l/i", null=True, blank=True)
    link_type = models.CharField(verbose_name="Тип ссылки", max_length=50, choices=LinkChoices.choices,
                                 default=LinkChoices.WEBSITE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Пользователь", related_name="links")
    collections = models.ManyToManyField("link_collections.Collection", verbose_name="Коллекция", related_name="links")

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"

    def __str__(self) -> str:
        return f"Ссылка - {self.link}"
