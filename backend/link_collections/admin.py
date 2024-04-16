from django.contrib.admin import register, ModelAdmin

from .models import Collection


@register(Collection)
class CollectionAdmin(ModelAdmin):
    pass
