from django.contrib.admin import register, ModelAdmin

from .models import Link


@register(Link)
class LinkAdmin(ModelAdmin):
    pass
