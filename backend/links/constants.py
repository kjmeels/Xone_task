from django.db.models import TextChoices


class LinkChoices(TextChoices):
    WEBSITE = "website", "сайт"
    BOOK = "book", "книга"
    ARTICLE = "article", "артикул"
    MUSIC = "music", "музыка"
    VIDEO = "video", "видео"
