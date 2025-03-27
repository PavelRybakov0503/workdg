from django import template

from config import settings

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f'{settings.MEDIA_URL}{path}'
    return '#'
